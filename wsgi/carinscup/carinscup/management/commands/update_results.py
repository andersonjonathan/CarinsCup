from django.core.management.base import BaseCommand
from django.conf import settings
from eventor_toolkit import Eventor
from carinscup.models import Competitor, Event, Race, Result, Organisation


class Command(BaseCommand):
    help = 'Updates organisation list.'

    def add_arguments(self, parser):
        parser.add_argument('--from',
            default='0000-01-01',
            help='Get results from this date.')
        parser.add_argument('--to',
            default='9999-12-31',
            help='Get results to this date.')

    def handle(self, *args, **options):
        from_date = options['from']
        to_date = options['to']

        e = Eventor(settings.API_KEY)
        for user in Competitor.objects.all():
            print(user)
            results = e.results_per_person(user.competitor_id, from_date=from_date, to_date=to_date)
            if type(results) != list:
                results = [results]
            for m in results:
                event_id = m['Event']['EventId']
                name = m['Event']['Name']['#text']
                event_form = m['Event']['@eventForm']
                event_status = m['Event']['EventStatusId']
                classification = m['Event']['EventClassificationId']
                start_date = m['Event']['StartDate']['Date']
                end_date = m['Event']['FinishDate']['Date']
                organisations = m['Event']['Organiser']['OrganisationId']
                event, created = Event.objects.get_or_create(
                    event_id=event_id,
                    defaults={'name': name,
                              'event_form': event_form,
                              'event_status': event_status,
                              'classification': classification,
                              'start_date': start_date,
                              'end_date': end_date,
                              })
                if event_form == 'RelaySingleDay':
                    continue
                if type(organisations) == list:
                    for o in organisations:
                        event.organisations.add(Organisation.objects.get(organisation_id=o))
                else:
                    event.organisations.add(Organisation.objects.get(organisation_id=organisations))
                event.save()

                class_race_info = m['ClassResult']['EventClass']['ClassRaceInfo']
                class_name = m['ClassResult']['EventClass']['ClassShortName']
                if type(class_race_info) == list:  # Multi race events ex o-ringen
                    nr_of_starts_dict = {}
                    course_length_dict = {}
                    for cri in class_race_info:
                        try:
                            nr_of_starts_dict[cri['EventRaceId']] = int(cri['@noOfStarts'])
                        except:
                            nr_of_starts_dict[cri['EventRaceId']] = None
                        try:
                            course_length_dict[cri['EventRaceId']] = int(cri['CourseLength'])
                        except:
                            course_length_dict[cri['EventRaceId']] = None
                    tmp = m['ClassResult']['PersonResult']
                    if type(tmp) != list:
                        tmp = [tmp]
                    for r in tmp:
                        event_race_id = r['RaceResult']['EventRace']['EventRaceId']
                        try:
                            race_name = r['RaceResult']['EventRace']['Name']['#text']
                        except:
                            race_name = None
                        try:
                            light_condition = r['RaceResult']['EventRace']['@raceLightCondition']
                        except:
                            light_condition = None
                        try:
                            distance = r['RaceResult']['EventRace']['@raceDistance']
                        except:
                            distance = None
                        try:
                            date = r['RaceResult']['EventRace']['RaceDate']['Date']
                        except:
                            date = None
                        race, created = Race.objects.get_or_create(
                            event=event,
                            event_race_id=event_race_id,
                            defaults={
                                'name': race_name,
                                'light_condition': light_condition,
                                'distance': distance,
                                'date': date,
                            })
                        course_length = course_length_dict[event_race_id]
                        nr_of_starts = nr_of_starts_dict[event_race_id]
                        try:
                            position = int(r['RaceResult']['Result']['ResultPosition'])
                        except:
                            position = None
                        try:
                            time = r['RaceResult']['Result']['Time']
                        except:
                            time = None
                        try:
                            time_diff = r['RaceResult']['Result']['TimeDiff']
                        except:
                            time_diff = None
                        try:
                            status = r['RaceResult']['Result']['CompetitorStatus']['@value']
                        except:
                            status = None
                        Result.objects.update_or_create(
                            competitor=user,
                            race=race,
                            defaults={
                                'course_length': course_length,
                                'class_name': class_name,
                                'nr_of_starts': nr_of_starts,
                                'position': position,
                                'time': time,
                                'time_diff': time_diff,
                                'status': status,
                            }
                        )
                else:  # Single race event
                    event_race_id = class_race_info['EventRaceId']
                    date = start_date
                    race, created = Race.objects.get_or_create(
                        event=event,
                        event_race_id=event_race_id,
                        defaults={
                            'date': date,
                        })
                    try:
                        course_length = m['ClassResult']['EventClass']['ClassRaceInfo']['CourseLength']
                    except:
                        course_length = None
                    try:
                        nr_of_starts = int(m['ClassResult']['EventClass']['ClassRaceInfo']['@noOfStarts'])
                    except:
                        nr_of_starts = None
                    try:
                        position = int(m['ClassResult']['PersonResult']['Result']['ResultPosition'])
                    except:
                        position = None

                    try:
                        time = m['ClassResult']['PersonResult']['Result']['Time']
                    except:
                        time = None
                    try:
                        time_diff = m['ClassResult']['PersonResult']['Result']['TimeDiff']
                    except:
                        time_diff = None
                    try:
                        status = m['ClassResult']['PersonResult']['Result']['CompetitorStatus']['@value']
                    except:
                        status = None
                    Result.objects.update_or_create(
                        competitor=user,
                        race=race,
                        defaults={
                            'course_length': course_length,
                            'class_name': class_name,
                            'nr_of_starts': nr_of_starts,
                            'position': position,
                            'time': time,
                            'time_diff': time_diff,
                            'status': status,
                        }
                    )
        Result.objects.update_cc_points()
