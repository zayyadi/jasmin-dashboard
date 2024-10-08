# Generated by Django 4.2.11 on 2024-08-22 20:20

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('service', models.CharField(max_length=100, verbose_name='Log Name')),
                ('method', models.CharField(max_length=10, verbose_name='Request Method')),
                ('params', models.TextField(default='{}', verbose_name='Request Parameters')),
                ('path', models.CharField(max_length=140, verbose_name='Log Path')),
                ('ip', models.GenericIPAddressField(verbose_name='IP Address')),
                ('user_agent', models.TextField(default='{}', verbose_name='User Agent')),
            ],
            options={
                'verbose_name': 'Activity Log',
                'verbose_name_plural': 'Activity Logs',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True, verbose_name='Is Enabled')),
                ('name', models.CharField(max_length=64, verbose_name='Currency Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('code', models.CharField(max_length=8, verbose_name='Currency Code')),
                ('code3', models.CharField(blank=True, max_length=8, null=True, verbose_name='Currency Code 3')),
                ('symbol', models.CharField(blank=True, max_length=8, null=True, verbose_name='Currency Symbol')),
                ('order', models.PositiveIntegerField(verbose_name='Currency Order')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
                'ordering': ('enabled', 'order'),
            },
        ),
        migrations.CreateModel(
            name='EmailServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('server', models.CharField(max_length=50, verbose_name='Server')),
                ('port', models.PositiveIntegerField(verbose_name='Port')),
                ('username', models.CharField(max_length=50, verbose_name='Username / Email')),
                ('password', models.CharField(max_length=50, verbose_name='Password')),
                ('ssl', models.BooleanField(default=True, verbose_name='SSL Support')),
                ('level', models.CharField(choices=[('admin', 'Administration'), ('security', 'Security'), ('info', 'Information')], default='info', max_length=24, verbose_name='Account Type')),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
            ],
            options={
                'verbose_name': 'Email Server',
                'verbose_name_plural': 'Email Servers',
            },
        ),
        migrations.CreateModel(
            name='FiltersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('TransparentFilter', 'TransparentFilter'), ('ConnectorFilter', 'ConnectorFilter'), ('UserFilter', 'UserFilter'), ('GroupFilter', 'GroupFilter'), ('SourceAddrFilter', 'SourceAddrFilter'), ('DestinationAddrFilter', 'DestinationAddrFilter'), ('ShortMessageFilter', 'ShortMessageFilter'), ('DateIntervalFilter', 'DateIntervalFilter'), ('TimeIntervalFilter', 'TimeIntervalFilter'), ('TagFilter', 'TagFilter'), ('EvalPyFilter', 'EvalPyFilter')], max_length=24, verbose_name='Type')),
                ('fid', models.CharField(max_length=24, unique=True, verbose_name='Filter ID')),
                ('parameters', models.TextField(verbose_name='Parameters')),
            ],
            options={
                'verbose_name': 'Filters',
                'verbose_name_plural': 'Filters',
                'db_table': 'tbl_filters',
            },
        ),
        migrations.CreateModel(
            name='GroupsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('gid', models.CharField(max_length=24, unique=True, verbose_name='Group ID')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Groups',
                'verbose_name_plural': 'Groups',
                'db_table': 'tbl_groups',
            },
        ),
        migrations.CreateModel(
            name='HTTPccmModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cid', models.CharField(help_text='Connector identifier', max_length=24, unique=True, verbose_name='Connector ID')),
                ('url', models.CharField(help_text='URL to be called with message parameters', max_length=128, verbose_name='URL')),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST')], max_length=16, verbose_name='Method')),
            ],
            options={
                'verbose_name': 'HTTP Client Connector',
                'verbose_name_plural': 'HTTP Client Connector',
                'db_table': 'tbl_httpccm',
            },
        ),
        migrations.CreateModel(
            name='MOInterceptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('DefaultInterceptor', 'DefaultInterceptor'), ('StaticMOInterceptor', 'StaticMOInterceptor')], max_length=30, verbose_name='Type')),
                ('order', models.CharField(help_text='Interceptor order, also used to identify Interceptor', max_length=24, verbose_name='Order')),
                ('script', models.CharField(help_text='Path to the Python script file', max_length=255, verbose_name='Script')),
            ],
            options={
                'verbose_name': 'MO Interceptor',
                'verbose_name_plural': 'MO Interceptor',
                'db_table': 'tbl_mointerceptor',
            },
        ),
        migrations.CreateModel(
            name='MORoutersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('DefaultRoute', 'DefaultRoute'), ('StaticMORoute', 'StaticMORoute'), ('RandomRoundrobinMORoute', 'RandomRoundrobinMORoute'), ('FailoverMORoute', 'FailoverMORoute')], max_length=24, verbose_name='Type')),
                ('order', models.CharField(help_text='Router order, also used to identify router', max_length=24, verbose_name='Order')),
            ],
            options={
                'verbose_name': 'MO Router',
                'verbose_name_plural': 'MO Router',
                'db_table': 'tbl_morouters',
            },
        ),
        migrations.CreateModel(
            name='MTInterceptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('DefaultInterceptor', 'DefaultInterceptor'), ('StaticMTInterceptor', 'StaticMTInterceptor')], max_length=30, verbose_name='Type')),
                ('order', models.CharField(help_text='Interceptor order, also used to identify Interceptor', max_length=24, verbose_name='Order')),
                ('script', models.CharField(help_text='Path to the Python script file', max_length=255, verbose_name='Script')),
            ],
            options={
                'verbose_name': 'MT Interceptor',
                'verbose_name_plural': 'MT Interceptor',
                'db_table': 'tbl_mtinterceptor',
            },
        ),
        migrations.CreateModel(
            name='MTRoutersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('DefaultRoute', 'DefaultRoute'), ('StaticMTRoute', 'StaticMTRoute'), ('RandomRoundrobinMTRoute', 'RandomRoundrobinMTRoute'), ('FailoverMTRoute', 'FailoverMTRoute')], max_length=24, verbose_name='Type')),
                ('order', models.CharField(help_text='Router order, also used to identify router', max_length=24, verbose_name='Order')),
                ('rate', models.FloatField(default=0.1, verbose_name='Rate')),
            ],
            options={
                'verbose_name': 'MT Router',
                'verbose_name_plural': 'MT Router',
                'db_table': 'tbl_mtrouters',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(max_length=40)),
                ('url', models.URLField()),
                ('email_list', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SMPPccmModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cid', models.CharField(help_text='Connector identifier', max_length=24, unique=True, verbose_name='Connector ID')),
                ('parameters', models.TextField(verbose_name='Parameters')),
                ('action', models.BooleanField(default=True, help_text='Start/Stop SMPP Connector', verbose_name='Action')),
            ],
            options={
                'verbose_name': 'SMPP Client Connector',
                'verbose_name_plural': 'SMPP Client Connector',
                'db_table': 'tbl_smppccm',
            },
        ),
        migrations.CreateModel(
            name='SubmitLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msgid', models.CharField(max_length=45, verbose_name='Message ID')),
                ('source_connector', models.CharField(max_length=15, verbose_name='Source Connector')),
                ('routed_cid', models.CharField(db_index=True, max_length=30, verbose_name='Routed CID')),
                ('source_addr', models.CharField(max_length=40, verbose_name='Source Address')),
                ('destination_addr', models.CharField(max_length=40, verbose_name='Destination Address')),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Rate')),
                ('pdu_count', models.PositiveIntegerField(default=1, verbose_name='PDU Count')),
                ('short_message', models.BinaryField(verbose_name='Short Message')),
                ('binary_message', models.BinaryField(verbose_name='Binary Message')),
                ('status', models.CharField(db_index=True, max_length=15, verbose_name='Status')),
                ('uid', models.CharField(db_index=True, max_length=15, verbose_name='UID')),
                ('trials', models.PositiveIntegerField(default=1, verbose_name='Trials')),
                ('created_at', models.DateTimeField(db_index=True, verbose_name='Created At')),
                ('status_at', models.DateTimeField(verbose_name='Status At')),
            ],
            options={
                'verbose_name': 'Submit Log',
                'verbose_name_plural': 'Submit Logs',
                'db_table': 'submit_log',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Tokenizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='This field is automatically determined by the system, do not interfere.', unique=True, verbose_name='Unique ID')),
                ('uidb64', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Tokenizer',
                'verbose_name_plural': 'Tokenizer',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=40)),
                ('url', models.URLField()),
                ('designated_bound', models.IntegerField(default=0)),
                ('email_list', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UsersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(max_length=24, unique=True, verbose_name='User ID')),
                ('username', models.CharField(max_length=24, verbose_name='Username')),
                ('password', models.CharField(max_length=24, verbose_name='Password')),
                ('parameters', models.TextField(verbose_name='Parameters')),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.groupsmodel', verbose_name='Group ID')),
            ],
            options={
                'verbose_name': 'Users',
                'verbose_name_plural': 'Users',
                'db_table': 'tbl_users',
            },
        ),
    ]
