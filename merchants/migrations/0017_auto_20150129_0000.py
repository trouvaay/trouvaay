# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0016_auto_20150123_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='neighborhood',
            field=models.CharField(default=b'na', max_length=80, choices=[(b'Alamo Square', b'Alamo Square'), (b'Anza Vista', b'Anza Vista'), (b'Ashbury Heights', b'Ashbury Heights'), (b'Balboa Terrace', b'Balboa Terrace'), (b'Bayview - Hunters Point', b'Bayview - Hunters Point'), (b'Berkeley', b'Berkeley'), (b'Bernal Heights', b'Bernal Heights'), (b'Buena Vista', b'Buena Vista'), (b'Castro', b'Castro'), (b'Chinatown', b'Chinatown'), (b'Civic Center', b'Civic Center'), (b'Cole Valley', b'Cole Valley'), (b'Corona Heights', b'Corona Heights'), (b'Cow Hollow', b'Cow Hollow'), (b'Crocker-Amazon', b'Crocker-Amazon'), (b'Diamond Heights', b'Diamond Heights'), (b'Dogpatch', b'Dogpatch'), (b'Duboce Triangle', b'Duboce Triangle'), (b'Embarcadero', b'Embarcadero'), (b'Excelsior', b'Excelsior'), (b'Fillmore', b'Fillmore'), (b'Financial District', b'Financial District'), (b"Fisherman's Wharf", b"Fisherman's Wharf"), (b'Forest Hill', b'Forest Hill'), (b'Glen Park', b'Glen Park'), (b'Haight-Ashbury', b'Haight-Ashbury'), (b'Hayes Valley', b'Hayes Valley'), (b'Ingleside', b'Ingleside'), (b'Ingleside Terraces', b'Ingleside Terraces'), (b'Inner Sunset', b'Inner Sunset'), (b'Jackson Square', b'Jackson Square'), (b'Japantown', b'Japantown'), (b'Lakeside', b'Lakeside'), (b'Lakeshore', b'Lakeshore'), (b'Laurel Heights', b'Laurel Heights'), (b'Lower Haight', b'Lower Haight'), (b'Lower Pacific Heights', b'Lower Pacific Heights'), (b'Lower Nob Hill', b'Lower Nob Hill'), (b'Marina', b'Marina'), (b'Merced Heights', b'Merced Heights'), (b'Merced Manor', b'Merced Manor'), (b'Miraloma Park', b'Miraloma Park'), (b'Mission Bay', b'Mission Bay'), (b'Mission District', b'Mission District'), (b'Mission Terrace', b'Mission Terrace'), (b'Monterey Heights', b'Monterey Heights'), (b'Mount Davidson', b'Mount Davidson'), (b'Nob Hill', b'Nob Hill'), (b'Noe Valley', b'Noe Valley'), (b'North Beach', b'North Beach'), (b'NoPa', b'NoPa'), (b'Oakland', b'Oakland'), (b'Oceanview', b'Oceanview'), (b'Outer Mission', b'Outer Mission'), (b'Outer Sunset', b'Outer Sunset'), (b'Outer Richmond', b'Outer Richmond'), (b'Pacific Heights', b'Pacific Heights'), (b'Parkmerced', b'Parkmerced'), (b'Parkside', b'Parkside'), (b'Portola', b'Portola'), (b'Potrero Hill', b'Potrero Hill'), (b'Presidio', b'Presidio'), (b'Presidio Heights', b'Presidio Heights'), (b'Rincon Hill', b'Rincon Hill'), (b'Russian Hill', b'Russian Hill'), (b'Saint Francis Wood', b'Saint Francis Wood'), (b'Sea Cliff', b'Sea Cliff'), (b'Sherwood Forest', b'Sherwood Forest'), (b'South Beach', b'South Beach'), (b'SoMa', b'SoMa'), (b'Sunnyside', b'Sunnyside'), (b'Sunset District', b'Sunset District'), (b'Telegraph Hill', b'Telegraph Hill'), (b'Tenderloin', b'Tenderloin'), (b'Twin Peaks', b'Twin Peaks'), (b'Union Square', b'Union Square'), (b'Visitacion Valley', b'Visitacion Valley'), (b'West Portal', b'West Portal'), (b'Western Addition', b'Western Addition'), (b'Westwood Highlands', b'Westwood Highlands'), (b'Westwood Park', b'Westwood Park'), (b'Yerba Buena', b'Yerba Buena')]),
            preserve_default=True,
        ),
    ]
