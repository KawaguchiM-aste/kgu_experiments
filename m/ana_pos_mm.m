clc;
lat = Position.latitude;
lon = Position.longitude;
alt = Position.altitude;
v = Position.speed;
t = seconds(Position.Timestamp - Position.Timestamp(1));
s = ["Time" "lat" "lon" "alt" "speed"];
df = table(t, lat, lon, alt, v, 'VariableNames', s);

L = 0;
for it=1:length(t)-1
    T = t(it+1)-t(it);
    L = L + v(it)*T;
end

subplot(4,1,[1,2,3])
title(['Length: ',num2str(L),"[m]"])
geoplot(lat,lon,'b-', 'LineWidth',2);
text(mean(lat),mean(lon),[num2str(L),"[m]"])
geobasemap topographic
subplot(4,1,4)
plot(t,v);
ylabel('speed [m/s]');
xlabel('Time [s]');

fname = "20260306_132942_ana_pos_result";
writetable(df, fname+'.xlsx');
saveas(gcf,fname+'.png');
% end of file