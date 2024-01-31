clc
clear

proj_info = funcReadProjectInfo('/home/chen/Desktop/remmina_share_folder/test_Barrioz2019_h0.2/','cylinder');
num_case = length(proj_info);

for i=1:num_case
    std_file_dir = [proj_info(i).dir '/result/output_file.std'];
    data = funcReadHomoOutput(std_file_dir,10,62);
    step_idx = funcGetCoalescenceStep(data);
    if step_idx>1
        ratio = data(step_idx,2)/500e6;
        scatter(proj_info(i).x2,0.9*ratio,'filled');
        hold on
    end
end
xlim([0.2 0.8]);
ylim([0 4]);
hold off
%%
clc
clear

x = 0:0.01:3;
% plot(x,(exp(2*x)+exp(-2*x))/2);
plot(x,sinh(x).^2+cosh(x).^2);
hold on
plot(x,1+2*x.^2+2/3*x.^4+4/45*x.^6+(2.^8/factorial(8))*x.^8);