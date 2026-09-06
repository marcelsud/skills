PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;

CREATE TABLE IF NOT EXISTS context_entries (
    id          INTEGER PRIMARY KEY,
    workspace   TEXT NOT NULL CHECK (length(trim(workspace)) > 0),
    kind        TEXT NOT NULL CHECK (kind IN (
                    'fact', 'decision', 'constraint', 'preference',
                    'finding', 'task', 'evidence'
                )),
    context_key TEXT,
    content     TEXT NOT NULL CHECK (length(trim(content)) > 0),
    source      TEXT,
    priority    INTEGER NOT NULL DEFAULT 0
                CHECK (priority BETWEEN -100 AND 100),
    created_at  INTEGER NOT NULL DEFAULT (unixepoch()),
    expires_at  INTEGER CHECK (expires_at IS NULL OR expires_at > created_at),
    state       TEXT NOT NULL DEFAULT 'active'
                CHECK (state IN ('active', 'superseded', 'expired'))
);

CREATE INDEX IF NOT EXISTS context_entries_active
    ON context_entries(workspace, state, expires_at, priority);

CREATE UNIQUE INDEX IF NOT EXISTS context_entries_current_key
    ON context_entries(workspace, context_key)
    WHERE context_key IS NOT NULL AND state = 'active';

CREATE TRIGGER IF NOT EXISTS context_entries_expire_key
BEFORE INSERT ON context_entries
WHEN NEW.context_key IS NOT NULL
BEGIN
    UPDATE context_entries
    SET state = 'expired'
    WHERE workspace = NEW.workspace
      AND context_key = NEW.context_key
      AND state = 'active'
      AND expires_at IS NOT NULL
      AND expires_at <= unixepoch();
END;

CREATE VIEW IF NOT EXISTS context_write AS
SELECT
    NULL AS operation,
    workspace,
    kind,
    context_key,
    content,
    source,
    priority,
    expires_at
FROM context_entries
WHERE 0;

CREATE TRIGGER IF NOT EXISTS context_write_insert
INSTEAD OF INSERT ON context_write
BEGIN
    SELECT RAISE(ABORT, 'operation must be remember or supersede')
    WHERE NEW.operation IS NULL
       OR NEW.operation NOT IN ('remember', 'supersede');

    UPDATE context_entries
    SET state = 'superseded'
    WHERE NEW.operation = 'supersede'
      AND workspace = NEW.workspace
      AND context_key = NEW.context_key
      AND state = 'active'
      AND (expires_at IS NULL OR expires_at > unixepoch());

    SELECT RAISE(ABORT, 'no active context key to supersede')
    WHERE NEW.operation = 'supersede' AND changes() <> 1;

    INSERT INTO context_entries (
        workspace,
        kind,
        context_key,
        content,
        source,
        priority,
        expires_at
    ) VALUES (
        NEW.workspace,
        NEW.kind,
        NEW.context_key,
        NEW.content,
        NEW.source,
        coalesce(NEW.priority, 0),
        NEW.expires_at
    );
END;

CREATE VIEW IF NOT EXISTS current_context AS
SELECT
    id,
    workspace,
    kind,
    context_key,
    content,
    source,
    priority,
    created_at,
    expires_at
FROM context_entries
WHERE state = 'active'
  AND (expires_at IS NULL OR expires_at > unixepoch());

CREATE VIEW IF NOT EXISTS context_keys AS
SELECT DISTINCT workspace, context_key
FROM context_entries
WHERE context_key IS NOT NULL;

CREATE TRIGGER IF NOT EXISTS context_keys_delete
INSTEAD OF DELETE ON context_keys
BEGIN
    DELETE FROM context_entries
    WHERE workspace = OLD.workspace
      AND context_key = OLD.context_key;
END;

CREATE VIRTUAL TABLE IF NOT EXISTS context_search USING fts5(
    context_key,
    content,
    source,
    content = 'context_entries',
    content_rowid = 'id',
    tokenize = 'unicode61'
);

CREATE TRIGGER IF NOT EXISTS context_entries_search_insert
AFTER INSERT ON context_entries
BEGIN
    INSERT INTO context_search(rowid, context_key, content, source)
    VALUES (NEW.id, NEW.context_key, NEW.content, NEW.source);
END;

CREATE TRIGGER IF NOT EXISTS context_entries_search_delete
AFTER DELETE ON context_entries
BEGIN
    INSERT INTO context_search(context_search, rowid, context_key, content, source)
    VALUES ('delete', OLD.id, OLD.context_key, OLD.content, OLD.source);
END;

CREATE TRIGGER IF NOT EXISTS context_entries_search_update
AFTER UPDATE OF context_key, content, source ON context_entries
BEGIN
    INSERT INTO context_search(context_search, rowid, context_key, content, source)
    VALUES ('delete', OLD.id, OLD.context_key, OLD.content, OLD.source);
    INSERT INTO context_search(rowid, context_key, content, source)
    VALUES (NEW.id, NEW.context_key, NEW.content, NEW.source);
END;
