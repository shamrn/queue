from api.models import Element


class ElementGetPid:
    """
    Поиск pid элемента, валидация входящих параметров
    """

    def check_missing_elements(self, data):
        """
        Проверка кол-ва элементов
        """
        self.required_params = ('first_name', 'last_name', 'midle_name', 'year', 'mouth', 'day')
        received_params = set(data)
        missing_params = set(self.required_params) - received_params
        if len(missing_params) > 0:
            return True

    def check_name(self, data):
        """
        Проверка имени
        """
        for param in self.required_params[0:3]:
            param_ = data[param].strip()
            if not param_.isalpha():
                return True

    def check_date(self, data):
        """
        Проверка даты
        """
        for param in self.required_params[3:6]:
            param_ = data[param].strip()
            if not param_.isdigit():
                return True

    def get_elements(self, data):
        """
        Получаем pid пациента
        """

        data = {key: value.strip() for key, value in data.items()}
        full_name = f"{data['last_name']} " \
                    f"{data['first_name']} " \
                    f"{data['midle_name']}"

        full_date = f"{data['year']}-" \
                    f"{data['mouth']}-" \
                    f"{data['day']}"

        element = Element.objects.filter(title__iexact=full_name, date_birth=full_date)

        if 'snils' in data:
            snils = data['snils']
            element = element.filter(snils=snils)

        if len(element) == 1:
            return element
        elif len(element) > 1:
            return False
