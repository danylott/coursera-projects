class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    @staticmethod
    def parse_body_whl(body_whl):
        return 'x'.split(body_whl)

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        parsed_body_whl = self.parse_body_whl(body_whl)
        try:
            self.body_width = float(parsed_body_whl[0])
            self.body_height = float(parsed_body_whl[1])
            self.body_length = float(parsed_body_whl[2])
        except ValueError:
            self.body_width = self.body_height = self.body_length = 0

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def create_car(data):
    if data[0] == 'car':
        return Car(data[1], data[3], data[5], data[2])
    elif data[0] == 'truck':
        return Truck()



def get_car_list(csv_filename):
    import csv

    with open(csv_filename, encoding='utf-8') as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            print(row)
            create_car(row)
    car_list = []
    return car_list


get_car_list('cars.csv')
