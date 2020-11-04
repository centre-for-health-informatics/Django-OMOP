# Django-OMOP

The OMOP Common Data Model implemented in Django.

![](docs/omop-erd.png)

### Set up Django

##### Clone repo and navigate to root directory of the repo.

`git clone https://github.com/airoscar/Django-OMOP`

##### Create environment from the environment.yml file using Conda:

`conda env create -f environment.yml`

##### Activate environment:

`conda activate omop`

##### Create a 'secrets' folder for storing environment variable (this folder is in gitignore):

`mkdir secrets`

##### Create a file for environment variables (Mac/Linux):

`nano secrets/env_vars.command`

##### In the file write the following (Mac/Linux):

```
export DJANGO_SECRET_KEY="RANDOM_STRING_FOR_DJANGO_HASHING"
export DJANGO_DEBUG=True
```

The DJANGO_SECRET_KEY should be a long string of random characters. Save and close the file.

##### Load environment variables from the file you just created (Mac/Linux):

`source ./secrets/env_vars.command`

##### Set up database:

`python manage.py migrate`
And you should see the database being created, by default this would be a `db.sqlite3` file located in the root directory.

### Initialize database

##### Register and download Athena vocabularies:

`https://athena.ohdsi.org/vocabulary/list`

##### Make a `OMOP_assets` folder in the `secrets` folder, and copy the following vocabulary csv files into location:

```
Django-OMOP/secrets/OMOP_assets/CONCEPT_ANCESTOR.csv
Django-OMOP/secrets/OMOP_assets/CONCEPT_CLASS.csv
Django-OMOP/secrets/OMOP_assets/CONCEPT_CPT4.csv
Django-OMOP/secrets/OMOP_assets/CONCEPT_RELATIONSHIP.csv
Django-OMOP/secrets/OMOP_assets/CONCEPT_SYNONYM.csv
Django-OMOP/secrets/OMOP_assets/CONCEPT.csv
Django-OMOP/secrets/OMOP_assets/DOMAIN.csv
Django-OMOP/secrets/OMOP_assets/DRUG_STRENGTH.csv
Django-OMOP/secrets/OMOP_assets/RELATIONSHIP.csv
Django-OMOP/secrets/OMOP_assets/VOCABULARY.csv
```

##### Run initialization:

To be continued...
