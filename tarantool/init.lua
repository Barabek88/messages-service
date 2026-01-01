box.cfg {
    listen = 3301,
    log_level = 5,
    memtx_memory = 1024 * 1024 * 1024,       
     -- ADD THESE FOR PERSISTENCE:
    -- wal_mode = 'write',              -- Enable Write-Ahead Log
    -- wal_dir = '/var/lib/tarantool',  -- Where to store WAL files
    -- memtx_dir = '/var/lib/tarantool', -- Where to store snapshots

        -- Snapshots
    -- checkpoint_interval = 3600,      -- Snapshot every 1 hour
    -- checkpoint_count = 2,            -- Keep last 2 snapshots
}

box.schema.user.passwd('admin', 'admin')
box.schema.user.grant('admin', 'read,write,execute', 'universe', nil, {if_not_exists = true})

box.once('init_spaces', function()
    messages:format({
        {name = 'id', type = 'string'},
        {name = 'conversation_id', type = 'string'},
        {name = 'sender_id', type = 'string'},
        {name = 'receiver_id', type = 'string'},
        {name = 'text', type = 'string'},
        {name = 'created_at', type = 'number'}
    })
    
    messages:create_index('primary', {parts = {'id'}, if_not_exists = true})
    messages:create_index('conversation', {parts = {'conversation_id', 'created_at'}, if_not_exists = true, unique = false})
end)

function send_message(conversation_id, sender_id, receiver_id, text)
    local uuid = require('uuid')
    local fiber = require('fiber')
    
    local message_id = uuid.str()
    local created_at = fiber.time()
    
    box.space.messages:insert({
        message_id,
        conversation_id,
        sender_id,
        receiver_id,
        text,
        created_at
    })
    
    return {id = message_id}
end

function get_conversation(conversation_id, limit)
    limit = limit or 50
    local messages = {}
    
    for _, tuple in box.space.messages.index.conversation:pairs({conversation_id}, {iterator = 'REQ'}) do
        if #messages >= limit then
            break
        end
        table.insert(messages, {
            from = tuple[3],
            to = tuple[4],
            text = tuple[5]
        })
    end
    
    return messages
end
