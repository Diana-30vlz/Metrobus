# Instrucciones para Claude — Proyecto Metrobus

## Contexto del proyecto

Es una API REST en Django 6 conectada a PostgreSQL.
- Base de datos operacional: `metrobus` (ya creada y corriendo en 127.0.0.1:5432)
- App Django: `GeneralTransactions`
- Directorio del backend: `MetrobusProject/MetrobusBack/`

## Tarea

Llenar las tablas del catálogo base en la BD `metrobus`.
Las tablas a llenar son: `merchants`, `bank_accounts`, `sellers`, `terminals`.
La tabla `transactions` y `gmr_files` NO se llenan (se llenan al procesar archivos CSV).

## Cómo ejecutarlo

Desde la carpeta `MetrobusProject/MetrobusBack/` corre:

```bash
python manage.py seed_catalog
```

Si las tablas ya tienen datos y quieres reemplazarlos:

```bash
python manage.py seed_catalog --force
```

## Datos que se insertan

### Merchants (4)

| RFC             | Razón social                    |
|-----------------|---------------------------------|
| BMN930209927    | B M NTE SA INS BAN M G F B      |
| ASM070207HP3    | CONDUENT SOLUTIONS MEX SRL CV   |
| MEX1312165H6    | MEXITELEFERICOS SA CV           |
| STC670419QY1    | SISTEMA TRANSPORTE COLECTIVO    |

### Bank Accounts (2)

| Número de cuenta | Moneda |
|-----------------|--------|
| 65508476998     | 484 (MXN) |
| 65509299803     | 484 (MXN) |

### Sellers (32)

| cod_seller | nombre                        | merchant     | cuenta      | linea     | tipo | esquema |
|------------|-------------------------------|--------------|-------------|-----------|------|---------|
| 8784421    | METROBUSL4TAPAMEX             | BMN930209927 | 65508476998 | NULL      | NULL | NULL    |
| 8784422    | METROBUSL4ECAMEX              | BMN930209927 | 65508476998 | NULL      | NULL | NULL    |
| 8792017    | METROBUSL3TVMAMEX             | BMN930209927 | 65508476998 | L3        | TVM  | AMEX    |
| 8792022    | METROBUSL3TAPAMEX             | BMN930209927 | 65508476998 | L3        | TAP  | AMEX    |
| 8792030    | METROBUSL2TAPAMEX             | BMN930209927 | 65508476998 | L2        | TAP  | AMEX    |
| 8792031    | METROBUSL1NTAPAMEX            | BMN930209927 | 65508476998 | L1 Norte  | TAP  | AMEX    |
| 8792032    | METROBUSL2TVMAMEX             | BMN930209927 | 65508476998 | L2        | TVM  | AMEX    |
| 8792033    | METROBUSL1NTVMAMEX            | BMN930209927 | 65508476998 | L1 Norte  | TVM  | AMEX    |
| 8792034    | METROBUSL1STVMAMEX            | BMN930209927 | 65508476998 | NULL      | NULL | NULL    |
| 8792298    | METROBUSL1STAPAMEX            | BMN930209927 | 65508476998 | L1 Sur    | TAP  | AMEX    |
| 9117976    | METROBUSL6TVMAMEX             | BMN930209927 | 65509299803 | L6        | TVM  | AMEX    |
| 9119992    | METROBUSL6TVMAMEX             | BMN930209927 | 65509299803 | L6        | TVM  | AMEX    |
| 9143344    | METROBUSL7TAPAMEX             | BMN930209927 | 65509299803 | L7        | TAP  | AMEX    |
| 9144481    | METROBUSL7TVMAMEX             | BMN930209927 | 65509299803 | L7        | TVM  | AMEX    |
| 9611166    | METROBUSL4TVM                 | BMN930209927 | 65509299803 | L4        | TVM  | NULL    |
| 9611206    | METROBUSL4TI                  | BMN930209927 | 65509299803 | L4        | TI   | NULL    |
| 9611233    | METROBUSL4TAP                 | BMN930209927 | 65509299803 | L4        | TAP  | NULL    |
| 9826919    | METROBUSL2CR                  | BMN930209927 | 65509299803 | NULL      | NULL | NULL    |
| 9826923    | METROBUSL2TVM                 | BMN930209927 | 65509299803 | NULL      | NULL | NULL    |
| 9052792    | CONDUENT SOLUT MEXICO SRL CV  | ASM070207HP3 | 65509299803 | NULL      | NULL | NULL    |
| 9070941    | METROBUSL5TAPAMEX NTE         | ASM070207HP3 | 65509299803 | L5 NTE    | TAP  | AMEX    |
| 9072329    | METROBUSL5TVMAMEX NTE         | ASM070207HP3 | 65509299803 | L5 NTE    | TVM  | AMEX    |
| 9072350    | METROBUSL5TVMAMEX SUR         | ASM070207HP3 | 65509299803 | L5 SUR    | TVM  | AMEX    |
| 9085711    | METROBUSL5TAPAMEX SUR         | ASM070207HP3 | 65509299803 | L5 SUR    | TAP  | AMEX    |
| 9513954    | MEXICABLEREDL1AMEXTAP         | MEX1312165H6 | 65509299803 | Red L1    | TAP  | AMEX    |
| 9753651    | MEXICABLEREDL1TAP             | MEX1312165H6 | 65509299803 | Red L1    | TAP  | NULL    |
| 9753653    | MEXICABLEREDL1CR              | MEX1312165H6 | 65509299803 | Red L1    | CR   | NULL    |
| 9753660    | MEXICABLEREDL1TVM             | MEX1312165H6 | 65509299803 | NULL      | NULL | NULL    |
| 9755023    | MEXICABLEREDL1TI              | MEX1312165H6 | 65509299803 | Red L1    | TI   | NULL    |
| 9458496    | METROTAPAMEX                  | STC670419QY1 | 65509299803 | General   | TAP  | AMEX    |
| 9508249    | METROTIAMEX                   | STC670419QY1 | 65509299803 | NULL      | NULL | NULL    |
| 9946846    | AUTOB METROCR                 | STC670419QY1 | 65509299803 | NULL      | NULL | NULL    |

### Terminals (26 filas — una por terminal física por afiliación)

| cod_seller | id_terminal |
|------------|-------------|
| 8784421    | PMX4421A    |
| 8792017    | PMX2017A    |
| 8792022    | PMX2022A    |
| 8792030    | PMX2030A    |
| 8792031    | PMX2031A    |
| 8792032    | PMX2032A    |
| 8792033    | PMX2033A    |
| 8792034    | PMX2034A    |
| 8792298    | PMX2298A    |
| 9117976    | PMX0673A    |
| 9119992    | PMXF3CDA    |
| 9143344    | PMX80E3A    |
| 9144481    | PMX88DAA    |
| 9611166    | 9611166     |
| 9611166    | PMXDC72A    |
| 9611206    | 9611206     |
| 9611233    | CONDUENT    |
| 9070941    | PMX2F42A    |
| 9072329    | PMXE026A    |
| 9072350    | PMX58FCA    |
| 9085711    | PMX2F17A    |
| 9513954    | PMX8F51A    |
| 9753651    | CONDUENT    |
| 9753653    | 9753653     |
| 9755023    | 9755023     |
| 9458496    | PMXB1B7A    |

## Modelos Django relevantes

```python
# GeneralTransactions/models.py (resumen de estructura)

class Merchant(models.Model):          # db_table = 'merchants'
    id            # UUID PK
    rfc           # VARCHAR unique  ← clave natural
    name          # VARCHAR

class BankAccount(models.Model):       # db_table = 'bank_accounts'
    id            # UUID PK
    num_account   # VARCHAR unique  ← clave natural
    currency_code # SMALLINT (484 = MXN)

class Seller(models.Model):            # db_table = 'sellers'
    id             # UUID PK
    merchant       # FK → Merchant
    bank_account   # FK → BankAccount
    cod_seller     # VARCHAR unique  ← clave natural del CSV (COD_SELLER)
    name           # VARCHAR
    line           # VARCHAR nullable
    terminal_type  # VARCHAR nullable  (TAP / TVM / TI / CR / EC)
    payment_scheme # VARCHAR nullable  (AMEX / NULL)

class Terminal(models.Model):          # db_table = 'terminals'
    id          # UUID PK
    seller      # FK → Seller
    id_terminal # VARCHAR  (ID_TERMINAL del CSV)
    # UNIQUE: (seller, id_terminal)
```

## Verificación rápida

```python
# Desde python manage.py shell
from GeneralTransactions.models import Merchant, BankAccount, Seller, Terminal
print(Merchant.objects.count())    # esperado: 4
print(BankAccount.objects.count()) # esperado: 2
print(Seller.objects.count())      # esperado: 32
print(Terminal.objects.count())    # esperado: 26
```
