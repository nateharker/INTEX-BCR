from django.contrib import admin
from .models import Organization, Skill, Joblisting, JobListingSkill, JobOffer, JobOfferSkill, User

admin.site.register(Organization)
admin.site.register(Skill)
admin.site.register(Joblisting)
admin.site.register(JobListingSkill)
admin.site.register(JobOffer)
admin.site.register(JobOfferSkill)
admin.site.register(User)