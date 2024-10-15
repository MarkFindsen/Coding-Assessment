from rest_framework import serializers

from ..admission.models import Course, Intake

class IntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intake
        fields = ['start_date', 'end_date']

class CourseSerializer(serializers.ModelSerializer):
    intakes = IntakeSerializer(many=True, read_only=True, source='intake_set')
    
    class Meta:
        model = Course
        fields = ['name', 'intakes']
