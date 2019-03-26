from django.db import models
import itertools 

class MeasurementManager(models.Manager):
    def get_table(self, start_datetime, end_datetime):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT level.observation_id, 
                        level.observation_datetime, 
                        level.level,
                        ripple.ripple, 
                        water_temperature.water_temperature,
                        air_temperature.air_temperature,
                        ice_thickness.ice_thickness,
                        precipitation.precipitation, 
                        precipitation.precipitation_type,
                        wind.wind_direction,
                        wind.wind_power,
                        water_object_condition.water_object_condition,
                        comment.comment
                FROM level 
                LEFT JOIN ripple ON 
                        level.observation_datetime = ripple.observation_datetime 
                        AND 
                        level.observation_id = ripple.observation_id
                LEFT JOIN water_temperature ON 
                        level.observation_datetime = water_temperature.observation_datetime 
                        AND 
                        level.observation_id = water_temperature.observation_id
                LEFT JOIN air_temperature ON 
                        level.observation_datetime = air_temperature.observation_datetime 
                        AND 
                        level.observation_id = air_temperature.observation_id  
                LEFT JOIN ice_thickness ON 
                        level.observation_datetime = ice_thickness.observation_datetime 
                        AND 
                        level.observation_id = ice_thickness.observation_id
                LEFT JOIN precipitation ON 
                        level.observation_datetime = precipitation.observation_datetime 
                        AND 
                        level.observation_id = precipitation.observation_id
                LEFT JOIN wind ON 
                        level.observation_datetime = wind.observation_datetime 
                        AND 
                        level.observation_id = wind.observation_id
                LEFT JOIN water_object_condition ON 
                        level.observation_datetime = water_object_condition.observation_datetime 
                        AND 
                        level.observation_id = water_object_condition.observation_id
                LEFT JOIN comment ON 
                        level.observation_datetime = comment.observation_datetime 
                        AND 
                        level.observation_id = comment.observation_id
                WHERE level.observation_datetime BETWEEN "%s" AND "%s";
            ''' % (start_datetime, end_datetime))
            description = cursor.description
            result = []
            data = {}
            column_names = [col[0] for col in description]
            for row in cursor:
                result.append(dict(zip(column_names, row)))
            
            data.update({'data' : result})
            return data
