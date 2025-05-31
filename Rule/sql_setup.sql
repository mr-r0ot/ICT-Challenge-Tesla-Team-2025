DROP FUNCTION IF EXISTS notify_event() CASCADE;
CREATE FUNCTION notify_event() RETURNS trigger AS $$
DECLARE
    data JSON;
BEGIN
    data = row_to_json(NEW);
    PERFORM pg_notify('db_events', data::TEXT);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- تریگر برای جدول تراکنش
CREATE TRIGGER trx_after_insert
AFTER INSERT ON transactions
FOR EACH ROW EXECUTE PROCEDURE notify_event();