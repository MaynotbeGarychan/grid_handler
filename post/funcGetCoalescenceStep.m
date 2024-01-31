function step_idx = funcGetCoalescenceStep(data)
step_idx = 0;
% obatin defromation gradient history
u11 = data(:,23);
u22 = data(:,24);
u33 = data(:,25);

% velocity list
num_step = length(u11);
v11 = zeros([num_step 1]);
v22 = zeros([num_step 1]);
v33 = zeros([num_step 1]);
for i=20:num_step
    v11(i) = u11(i) - u11(i-1);
    v22(i) = u22(i) - u22(i-1);
    v33(i) = u33(i) - u33(i-1);
    if (max([abs(v22(i)) abs(v33(i))]) < 0.05 * abs(v11(i)))
        step_idx = i;
        return
    end
end
return
end

