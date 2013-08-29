data = importdata('nb_of_observed_events_per_users.csv', ',', 1);

bar(data.data(1:end, 1))
title('Number of observed events per student')
xlabel('Student number')
ylabel('Number of observed events')

% set(gca,'XTickLabel',data.textdata(2:end, 1))
%TODO: How can I rotate my X-axis tick labels and place an X-label on my plot?
% http://www.mathworks.com/support/solutions/en/data/1-15TK6/
print('-dpng','-r300', ['nb_of_observed_events_per_users'])
saveas(figure(1), 'nb_of_observed_events_per_users', 'fig')
