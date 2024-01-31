function proj_info = funcReadProjectInfo(project_dir,aString)

proj_info = struct('dir',{},'x1',{},'x2',{},'W1',{},'W2',{},'alpha',{});


items = dir(project_dir);
proj_info = {};

for i = 1:numel(items)
    if items(i).isdir && startsWith(items(i).name, aString)
        proj_info(end+1).dir = fullfile(project_dir, items(i).name);
        % extract values
        parts = strsplit(items(i).name, '_');
        for j = 2:2:numel(parts)
            field_name = parts{j};
            field_value = str2double(parts{j + 1});
            if ~isnan(field_value)
                proj_info(end).(field_name) = field_value;
            end
        end
    end
end


end

