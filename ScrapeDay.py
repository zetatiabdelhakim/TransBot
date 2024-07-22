from Train import Train
import csv


class ScrapeDay:
    def __init__(self, states, file_name, date):
        self.all_states = ["ADDAKHLA SUPRATOURS", "AGADIR (SUPRAT.)", "BENGUERIR", 'CASA PORT',
                           'CASA VOYAGEURS', 'EL JADIDA', 'ESSAOUIRA SUPRATOURS', 'FES',
                           'GUELMIMA', 'KENITRA', 'KHOURIBGA', 'LAAYOUNE SUPRATOURS',
                           'MARRAKECH', 'MARTIL', 'MEKNES','MIDELT (SUPRAT.)', 'MOHAMMEDIA',
                           'OUJDA', 'TETOUAN SUPRATOURS', 'RABAT AGDAL', 'RABAT VILLE',
                           'SAFI', 'SALE', 'SETTAT', 'TANGER',]

        self.header = ["gare de depart", "gare d'arrivee", "date de voyage",
                       "heure de depart", "heure d'arrivee", "prix",
                       "correspondance 1", "correspondance 2",
                       "correspondance 3", "correspondance 4"]

        self.file = file_name
        self.date = date
        self.trains = []
        for state1 in states:
            for state2 in self.all_states:
                if state1 == state2:
                    continue
                self.trains.append(Train(state1, state2))

    def run(self):
        data_to_save = []
        for train in self.trains:
            count = 0
            while count < 3:
                try:
                    data = train.scrape_day(self.date)
                    data_to_save.extend(data)

                    break
                except:
                    count += 1
            else:
                data_to_save.append([train.depart, train.arrive, self.date] + [None] * 7)
        with open(self.file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            writer.writerows(data_to_save)
