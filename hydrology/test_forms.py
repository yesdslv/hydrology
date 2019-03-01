from django.test import TestCase


from .forms import RHP1Form, RHP2Form, RHP3Form, LHP1Form, LHP2Form, SHP1Form, SHP2Form 


class ObservationFormTest(TestCase):

    ##Form for Речной пост 1 разряд
    def test_RHP1_form_contains_all_observation_for_his_type(self):
        form = RHP1Form()
        self.assertIn('name="level"', form.as_p())
        self.assertIn('name="air_temperature"', form.as_p())
        self.assertIn('name="water_temperature"', form.as_p())
        self.assertIn('name="condition"', form.as_p())
        self.assertIn('name="ice_thickness"', form.as_p())
        self.assertIn('name="precipitation"', form.as_p())
        self.assertIn('name="precipitation_type"', form.as_p())
        self.assertIn('name="wind_power"', form.as_p())
        self.assertIn('name="wind_direction"', form.as_p())

    ##Form for Речной пост 2 разряд
    def test_RHP2_form_contains_all_observation_for_his_type(self):
        form = RHP2Form()
        self.assertIn('name="level"', form.as_p())
        self.assertIn('name="water_temperature"', form.as_p())
        self.assertIn('name="air_temperature"', form.as_p())
        self.assertIn('name="condition"', form.as_p())
        self.assertIn('name="ice_thickness"', form.as_p())
        self.assertIn('name="precipitation"', form.as_p())
        self.assertIn('name="precipitation_type"', form.as_p())
        self.assertIn('name="wind_power"', form.as_p())
        self.assertIn('name="wind_direction"', form.as_p())

    ##Form for Речной пост 3 разряд
    def test_RHP3_form_contains_all_observation_for_his_type(self):
        form = RHP3Form()
        self.assertIn('name="level"', form.as_p())
        self.assertIn('name="water_temperature"', form.as_p())
        self.assertIn('name="air_temperature"', form.as_p())
        self.assertIn('name="condition"', form.as_p())
        self.assertIn('name="ice_thickness"', form.as_p())
        self.assertIn('name="wind_power"', form.as_p())
        self.assertIn('name="wind_direction"', form.as_p())

    ##Form for Озерный пост 1 разряд
    def test_LHP1_form_contains_all_observation_for_his_type(self):
        form = LHP1Form()
        self.assertIn('name="level"', form.as_p())
        self.assertIn('name="ripple"', form.as_p())
        self.assertIn('name="water_temperature"', form.as_p())
        self.assertIn('name="air_temperature"', form.as_p())
        self.assertIn('name="condition"', form.as_p())
        self.assertIn('name="ice_thickness"', form.as_p())
        self.assertIn('name="precipitation"', form.as_p())
        self.assertIn('name="precipitation_type"', form.as_p())
        self.assertIn('name="wind_power"', form.as_p())
        self.assertIn('name="wind_direction"', form.as_p())

    ##Form for Озерный пост 2 разряд
    def test_LHP2_form_contains_all_observation_for_his_type(self):
        form = LHP2Form()
        self.assertIn('name="level"', form.as_p())
        self.assertIn('name="ripple"', form.as_p())
        self.assertIn('name="water_temperature"', form.as_p())
        self.assertIn('name="air_temperature"', form.as_p())
        self.assertIn('name="condition"', form.as_p())
        self.assertIn('name="ice_thickness"', form.as_p())
        self.assertIn('name="precipitation"', form.as_p())
        self.assertIn('name="precipitation_type"', form.as_p())
        self.assertIn('name="wind_power"', form.as_p())
        self.assertIn('name="wind_direction"', form.as_p())

    ##Form for морской пост 1 разряд
    def test_SHP1_form_contains_all_observation_for_his_type(self):
        form = SHP1Form()
        self.assertIn('name="level"', form.as_p())
        self.assertIn('name="ripple"', form.as_p())
        self.assertIn('name="water_temperature"', form.as_p())
        self.assertIn('name="air_temperature"', form.as_p())
        self.assertIn('name="condition"', form.as_p())
        self.assertIn('name="ice_thickness"', form.as_p())
        self.assertIn('name="precipitation"', form.as_p())
        self.assertIn('name="precipitation_type"', form.as_p())
        self.assertIn('name="wind_power"', form.as_p())
        self.assertIn('name="wind_direction"', form.as_p())
    
    ##Form for морской пост 2 разряд
    def test_SHP2_form_contains_all_observation_for_his_type(self):
        form = SHP2Form()
        self.assertIn('name="level"', form.as_p())
        self.assertIn('name="ripple"', form.as_p())
        self.assertIn('name="water_temperature"', form.as_p())
        self.assertIn('name="air_temperature"', form.as_p())
        self.assertIn('name="condition"', form.as_p())
        self.assertIn('name="ice_thickness"', form.as_p())
        self.assertIn('name="precipitation"', form.as_p())
        self.assertIn('name="precipitation_type"', form.as_p())
        self.assertIn('name="wind_power"', form.as_p())
        self.assertIn('name="wind_direction"', form.as_p())
