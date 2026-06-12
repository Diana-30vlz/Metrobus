-- ============================================================
--  BD ANALÍTICA: daily
--  Ejecutar en PostgreSQL con un superusuario
--  Paso 1: crear la base de datos (si no existe)
-- ============================================================

-- Ejecuta esto conectado a postgres o cualquier otra BD:
-- CREATE DATABASE daily;

-- ============================================================
--  Paso 2: conectarte a la BD daily y ejecutar lo siguiente
--  \c daily
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
--  daily_summary
--  Un registro por (settlement_date + cod_seller).
--  Contiene los totales del día con desgloses por comercio,
--  afiliación y cuenta bancaria para facilitar conciliación.
-- ============================================================

CREATE TABLE IF NOT EXISTS daily_summary (
    id                  UUID            PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Dimensiones de negocio (denormalizadas para consultas directas)
    settlement_date     DATE            NOT NULL,
    merchant_rfc        VARCHAR(20)     NOT NULL,
    merchant_name       VARCHAR(200),
    cod_seller          VARCHAR(20)     NOT NULL,
    seller_name         VARCHAR(100),
    num_bank_account    VARCHAR(30),

    -- Conteos de transacciones
    tx_count            INTEGER         NOT NULL DEFAULT 0,
    tx_approved         INTEGER         NOT NULL DEFAULT 0,
    tx_captured         INTEGER         NOT NULL DEFAULT 0,
    tx_refund           INTEGER         NOT NULL DEFAULT 0,
    tx_other_status     INTEGER         NOT NULL DEFAULT 0,

    -- Montos principales
    amt_gross_total     NUMERIC(18, 2)  NOT NULL DEFAULT 0,
    amt_net_total       NUMERIC(18, 2)  NOT NULL DEFAULT 0,
    amt_fee_total       NUMERIC(18, 2)  NOT NULL DEFAULT 0,
    amt_vat_total       NUMERIC(18, 2)  NOT NULL DEFAULT 0,
    amt_mdr_total       NUMERIC(18, 4)  NOT NULL DEFAULT 0,

    -- Desglose por marca de tarjeta
    visa_count          INTEGER         NOT NULL DEFAULT 0,
    mastercard_count    INTEGER         NOT NULL DEFAULT 0,
    amex_count          INTEGER         NOT NULL DEFAULT 0,
    carnet_count        INTEGER         NOT NULL DEFAULT 0,
    other_brand_count   INTEGER         NOT NULL DEFAULT 0,

    -- Montos por marca de tarjeta
    visa_gross          NUMERIC(18, 2)  NOT NULL DEFAULT 0,
    mastercard_gross    NUMERIC(18, 2)  NOT NULL DEFAULT 0,
    amex_gross          NUMERIC(18, 2)  NOT NULL DEFAULT 0,
    carnet_gross        NUMERIC(18, 2)  NOT NULL DEFAULT 0,

    -- Desglose por modo de lectura
    contactless_count   INTEGER         NOT NULL DEFAULT 0,
    chip_count          INTEGER         NOT NULL DEFAULT 0,
    other_mode_count    INTEGER         NOT NULL DEFAULT 0,

    -- Referencia al archivo origen
    gmr_file            VARCHAR(200),

    -- Auditoría
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_daily_summary UNIQUE (settlement_date, cod_seller, gmr_file)
);

-- Índices para las consultas más frecuentes
CREATE INDEX IF NOT EXISTS idx_ds_date
    ON daily_summary (settlement_date DESC);

CREATE INDEX IF NOT EXISTS idx_ds_merchant
    ON daily_summary (merchant_rfc, settlement_date DESC);

CREATE INDEX IF NOT EXISTS idx_ds_seller
    ON daily_summary (cod_seller, settlement_date DESC);

CREATE INDEX IF NOT EXISTS idx_ds_bank
    ON daily_summary (num_bank_account, settlement_date DESC);

-- ============================================================
--  Trigger: mantiene updated_at al día automáticamente
-- ============================================================

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_daily_summary_updated_at
    BEFORE UPDATE ON daily_summary
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
