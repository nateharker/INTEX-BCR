from django.db import models

class Organization(models.Model) :
    # existing data below
    company_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=100)
    size = models.CharField(max_length=2)
    sector = models.CharField(max_length=2)

    def __str__(self) :
        return(self.company_name)

class Skill(models.Model) :
    description = models.CharField(max_length=40)

    def __str__(self) :
        return(self.description)

class Joblisting(models.Model) :
    job_title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    contracts = models.CharField(max_length=50)
    status = models.CharField(max_length=15)
    skills = models.ManyToManyField('Skill', through='JobListingSkill')

    def __str__(self) :
        return(self.job_title + ' at ' + str(self.organization))

class JobListingSkill(models.Model) :
    job_listing = models.ForeignKey(Joblisting, on_delete=models.CASCADE)
    # assumes that if there isn't a skill, we don't want this record
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance = models.SmallIntegerField()

    def __str__(self) :
        return(str(self.job_listing) + ' seeking ' + str(self.skill))

class User(models.Model) :
    # existing data below
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    # organization = models.OneToOneField(Organization, models.CASCADE)
    # job_title = models.CharField(max_length=50)
    
    def __str__(self) :
        return(self.first_name + " " + self.last_name)
        
    @property
    def full_name(self) :
        return (self.first_name + " " + self.last_name)


class JobOffer(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    contracts = models.CharField(max_length=2)
    matching_skills = models.SmallIntegerField()
    status = models.CharField(max_length=15)
    skills = models.ManyToManyField('Skill', through='JobOfferSkill')

    def __str__(self) :
        return(self.job_title + " from " + str(self.organization) + " to " + str(self.user))

class JobOfferSkill(models.Model) :
    joboffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    # assumes that if there isn't a skill, we don't want this record
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.SmallIntegerField()

    def __str__(self) :
        return(str(self.skill) + ' listed on ' + str(self.joboffer))