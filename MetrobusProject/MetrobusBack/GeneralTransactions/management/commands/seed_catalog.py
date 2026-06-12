import uuid
from django.core.management.base import BaseCommand
from GeneralTransactions.models import Merchant, BankAccount, Seller, Terminal


MERCHANTS = [
    {'rfc': 'BMN930209927', 'name': 'B M NTE SA INS BAN M G F B'},
    {'rfc': 'ASM070207HP3', 'name': 'CONDUENT SOLUTIONS MEX SRL CV'},
    {'rfc': 'MEX1312165H6', 'name': 'MEXITELEFERICOS SA CV'},
    {'rfc': 'STC670419QY1', 'name': 'SISTEMA TRANSPORTE COLECTIVO'},
]

BANK_ACCOUNTS = [
    {'num_account': '65508476998', 'currency_code': 484},
    {'num_account': '65509299803', 'currency_code': 484},
]

# (cod_seller, name, merchant_rfc, bank_account, line, terminal_type, payment_scheme)
SELLERS = [
    # BMN - cuenta 65508476998
    ('8784421', 'METROBUSL4TAPAMEX',            'BMN930209927', '65508476998', None,       None,  None),
    ('8784422', 'METROBUSL4ECAMEX',             'BMN930209927', '65508476998', None,       None,  None),
    ('8792017', 'METROBUSL3TVMAMEX',            'BMN930209927', '65508476998', 'L3',       'TVM', 'AMEX'),
    ('8792022', 'METROBUSL3TAPAMEX',            'BMN930209927', '65508476998', 'L3',       'TAP', 'AMEX'),
    ('8792030', 'METROBUSL2TAPAMEX',            'BMN930209927', '65508476998', 'L2',       'TAP', 'AMEX'),
    ('8792031', 'METROBUSL1NTAPAMEX',           'BMN930209927', '65508476998', 'L1 Norte', 'TAP', 'AMEX'),
    ('8792032', 'METROBUSL2TVMAMEX',            'BMN930209927', '65508476998', 'L2',       'TVM', 'AMEX'),
    ('8792033', 'METROBUSL1NTVMAMEX',           'BMN930209927', '65508476998', 'L1 Norte', 'TVM', 'AMEX'),
    ('8792034', 'METROBUSL1STVMAMEX',           'BMN930209927', '65508476998', None,       None,  None),
    ('8792298', 'METROBUSL1STAPAMEX',           'BMN930209927', '65508476998', 'L1 Sur',   'TAP', 'AMEX'),
    # BMN - cuenta 65509299803
    ('9117976', 'METROBUSL6TVMAMEX',            'BMN930209927', '65509299803', 'L6',       'TVM', 'AMEX'),
    ('9119992', 'METROBUSL6TVMAMEX',            'BMN930209927', '65509299803', 'L6',       'TVM', 'AMEX'),
    ('9143344', 'METROBUSL7TAPAMEX',            'BMN930209927', '65509299803', 'L7',       'TAP', 'AMEX'),
    ('9144481', 'METROBUSL7TVMAMEX',            'BMN930209927', '65509299803', 'L7',       'TVM', 'AMEX'),
    ('9611166', 'METROBUSL4TVM',                'BMN930209927', '65509299803', 'L4',       'TVM', None),
    ('9611206', 'METROBUSL4TI',                 'BMN930209927', '65509299803', 'L4',       'TI',  None),
    ('9611233', 'METROBUSL4TAP',                'BMN930209927', '65509299803', 'L4',       'TAP', None),
    ('9826919', 'METROBUSL2CR',                 'BMN930209927', '65509299803', None,       None,  None),
    ('9826923', 'METROBUSL2TVM',                'BMN930209927', '65509299803', None,       None,  None),
    # ASM - cuenta 65509299803
    ('9052792', 'CONDUENT SOLUT MEXICO SRL CV', 'ASM070207HP3', '65509299803', None,       None,  None),
    ('9070941', 'METROBUSL5TAPAMEX NTE',        'ASM070207HP3', '65509299803', 'L5 NTE',   'TAP', 'AMEX'),
    ('9072329', 'METROBUSL5TVMAMEX NTE',        'ASM070207HP3', '65509299803', 'L5 NTE',   'TVM', 'AMEX'),
    ('9072350', 'METROBUSL5TVMAMEX SUR',        'ASM070207HP3', '65509299803', 'L5 SUR',   'TVM', 'AMEX'),
    ('9085711', 'METROBUSL5TAPAMEX SUR',        'ASM070207HP3', '65509299803', 'L5 SUR',   'TAP', 'AMEX'),
    # MEX - cuenta 65509299803
    ('9513954', 'MEXICABLEREDL1AMEXTAP',        'MEX1312165H6', '65509299803', 'Red L1',   'TAP', 'AMEX'),
    ('9753651', 'MEXICABLEREDL1TAP',            'MEX1312165H6', '65509299803', 'Red L1',   'TAP', None),
    ('9753653', 'MEXICABLEREDL1CR',             'MEX1312165H6', '65509299803', 'Red L1',   'CR',  None),
    ('9753660', 'MEXICABLEREDL1TVM',            'MEX1312165H6', '65509299803', None,       None,  None),
    ('9755023', 'MEXICABLEREDL1TI',             'MEX1312165H6', '65509299803', 'Red L1',   'TI',  None),
    # STC - cuenta 65509299803
    ('9458496', 'METROTAPAMEX',                 'STC670419QY1', '65509299803', 'General',  'TAP', 'AMEX'),
    ('9508249', 'METROTIAMEX',                  'STC670419QY1', '65509299803', None,       None,  None),
    ('9946846', 'AUTOB METROCR',                'STC670419QY1', '65509299803', None,       None,  None),
]

# (cod_seller, id_terminal)
TERMINALS = [
    ('8784421', 'PMX4421A'),
    ('8792017', 'PMX2017A'),
    ('8792022', 'PMX2022A'),
    ('8792030', 'PMX2030A'),
    ('8792031', 'PMX2031A'),
    ('8792032', 'PMX2032A'),
    ('8792033', 'PMX2033A'),
    ('8792034', 'PMX2034A'),
    ('8792298', 'PMX2298A'),
    ('9117976', 'PMX0673A'),
    ('9119992', 'PMXF3CDA'),
    ('9143344', 'PMX80E3A'),
    ('9144481', 'PMX88DAA'),
    ('9611166', '9611166'),
    ('9611166', 'PMXDC72A'),
    ('9611206', '9611206'),
    ('9611233', 'CONDUENT'),
    ('9070941', 'PMX2F42A'),
    ('9072329', 'PMXE026A'),
    ('9072350', 'PMX58FCA'),
    ('9085711', 'PMX2F17A'),
    ('9513954', 'PMX8F51A'),
    ('9753651', 'CONDUENT'),
    ('9753653', '9753653'),
    ('9755023', '9755023'),
    ('9458496', 'PMXB1B7A'),
]


class Command(BaseCommand):
    help = 'Carga el catálogo base: merchants, bank_accounts, sellers y terminals.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Borra los datos existentes antes de insertar.',
        )

    def handle(self, *args, **options):
        if options['force']:
            Terminal.objects.all().delete()
            Seller.objects.all().delete()
            BankAccount.objects.all().delete()
            Merchant.objects.all().delete()
            self.stdout.write(self.style.WARNING('Datos anteriores eliminados.'))

        if Merchant.objects.exists():
            self.stdout.write(self.style.WARNING(
                'Las tablas ya tienen datos. Usa --force para reemplazarlos.'
            ))
            return

        merchant_map = {}
        for m in MERCHANTS:
            obj, _ = Merchant.objects.get_or_create(
                rfc=m['rfc'], defaults={'id': uuid.uuid4(), 'name': m['name']}
            )
            merchant_map[m['rfc']] = obj
        self.stdout.write(f'  Merchants:    {len(merchant_map)}')

        ba_map = {}
        for ba in BANK_ACCOUNTS:
            obj, _ = BankAccount.objects.get_or_create(
                num_account=ba['num_account'],
                defaults={'id': uuid.uuid4(), 'currency_code': ba['currency_code']},
            )
            ba_map[ba['num_account']] = obj
        self.stdout.write(f'  BankAccounts: {len(ba_map)}')

        seller_map = {}
        for cod, name, mrfc, banum, line, ttype, pscheme in SELLERS:
            obj, _ = Seller.objects.get_or_create(
                cod_seller=cod,
                defaults={
                    'id': uuid.uuid4(),
                    'merchant': merchant_map[mrfc],
                    'bank_account': ba_map[banum],
                    'name': name,
                    'line': line,
                    'terminal_type': ttype,
                    'payment_scheme': pscheme,
                },
            )
            seller_map[cod] = obj
        self.stdout.write(f'  Sellers:      {len(seller_map)}')

        terminal_count = 0
        for cod, id_terminal in TERMINALS:
            _, created = Terminal.objects.get_or_create(
                seller=seller_map[cod],
                id_terminal=id_terminal,
                defaults={'id': uuid.uuid4()},
            )
            if created:
                terminal_count += 1
        self.stdout.write(f'  Terminals:    {terminal_count}')

        self.stdout.write(self.style.SUCCESS('Catálogo cargado correctamente.'))
