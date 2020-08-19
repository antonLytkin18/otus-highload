box.schema.space.create('512', { if_not_exists = true })
box.space[512]:create_index('primary', { type = "TREE", unique = true, parts = { 1, 'unsigned' }, if_not_exists = true })

box.schema.space.create('513', { if_not_exists = true })
box.space[513]:create_index('primary', { type = "TREE", unique = true, parts = { 1, 'unsigned' }, if_not_exists = true })
box.space[513]:create_index('name_idx', { type = 'TREE', unique = false, parts = { 2, 'string' }, if_not_exists = true })
box.space[513]:create_index('last_name_idx', { type = 'TREE', unique = false, parts = { 3, 'string' }, if_not_exists = true })

function follower_find_all(last_name, name, limit, offset)
    local result = {}
    local total_cnt = 0
    local table_cnt = 0
    for _, tuple in box.space[513].index.last_name_idx:pairs({ last_name }, { iterator = 'GE' }) do
        if string.startswith(tuple[3], last_name, 1, -1) and string.startswith(tuple[2], name, 1, -1) then
            if total_cnt >= offset then
                table.insert(result, tuple)
                table_cnt = table_cnt + 1
            end
        end
        if table_cnt >= limit then
            return result
        end
        total_cnt = total_cnt + 1

    end
    return result
end

function follower_count_all(last_name, name)
    local total_cnt = 0
    for _, tuple in box.space[513].index.last_name_idx:pairs({ last_name }, { iterator = 'GE' }) do
        if string.startswith(tuple[3], last_name, 1, -1) and string.startswith(tuple[2], name, 1, -1) then
            total_cnt = total_cnt + 1
        end
    end
    return total_cnt
end

function count_all(space)
    return box.space[space]:count()
end