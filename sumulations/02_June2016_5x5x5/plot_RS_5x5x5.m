figure(1)

% reformmating into 3D array

% big_result(1...) = TP
% big_result(2..) = Chl

%mid_run = (datenum(m_stop)-datenum(m_start))/2;
post_big_run = (squeeze(big_result(2,:,400:end)));  % maximum of , remove singleton, take the chl, all runs, remove 1 yr spin up
post_big_run(imag(post_big_run) ~= 0) = NaN; % removing imaginary numbers
post_big_run(post_big_run<0) = NaN;

post_big_vector = max(post_big_run,[],2);
post_big_vector(post_big_vector<0) = 0;

% taking the middle TP_reduction course (constant) out of each TP_red.
% basically we do not plot the effect of TP reduction rates 
 
% taking only the TP at constant Tred 
TvsP = reshape(post_big_vector(3:5:end),[5, 5]); %  starting from col 3, it takes every 5th value, then reshapes the 1x25 into a 5x5

contourf(TvsP)
% chl at the end (8000)

% plot RS

figure (2)

x = [1:length(post_big_run(1,:))];
plot_id = 1;

for i = 1:5
    
    
    
    subplot(2,3,i)
    
    plot(x,post_big_run(plot_id:plot_id+4,:))
    plot_id =  plot_id+5;
end


