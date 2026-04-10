clear all
close all

f0 = 200;
Fs = 8000;
Tdur = 5.0;
T_win = 0.1;

dt = 1/Fs;
t = [0:dt:Tdur-dt];

x = sin(2*pi*f0*t);
x(x>=0) = 1/2;
x(x<0) = -1/2;
fname = ['rect_',num2str(f0),'Hz_',num2str(Tdur),'s.mp3']
sound(x,Fs);
audiowrite(fname, x, Fs);

nd = length(x);
itmid = round(nd/2);
iwinh = round(T_win*Fs/2);
subplot(2,1,1)
plot(t,x,'b-')
hold on
plot(t(itmid-iwinh:itmid+iwinh),x(itmid-iwinh:itmid+iwinh),'r-')
subplot(2,1,2)
plot(t(itmid-iwinh:itmid+iwinh),x(itmid-iwinh:itmid+iwinh),'r-')
ylim([-0.8 0.8])
xlabel('Time [s]')
fname = ['sin_',num2str(f0),'Hz_',num2str(Tdur),'s.png']
saveas(gcf, fname)
% end of file