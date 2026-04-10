clear all
close all

f0 = 200;
Fs = 8000;
Tdur = 5;
T_win = 0.2;
f_diff = 10.0;

dt = 1/Fs;
t = [0:dt:5-dt];

x1 = sin(2*pi*(f0-f_diff)*t);
x2 = sin(2*pi*(f0)*t);
x = x1+x2;
fname = ['un_',num2str(f0),'-',num2str(f0-f_diff),'Hz_',num2str(Tdur),'s.mp3']
sound(x,Fs);
audiowrite(fname, x, Fs);

nd = length(x);
itmid = round(nd/2);
iwinh = round(T_win*Fs/2);
itran = round(rand(1)*(nd-iwinh));

subplot(4,1,1)
plot(t,x,'b-')
hold on
plot(t(itmid-iwinh:itmid+iwinh),x(itmid-iwinh:itmid+iwinh),'r-')
plot(t(itran-iwinh:itran+iwinh),x(itran-iwinh:itran+iwinh),'y-')
hold off
subplot(4,1,2)
plot(t(itmid-iwinh:itmid+iwinh),x(itmid-iwinh:itmid+iwinh),'r-')
axis tight
subplot(4,1,3)
hold on
plot(t(itmid-iwinh:itmid+iwinh),x1(itmid-iwinh:itmid+iwinh),'Color',[0,0.5,0])
plot(t(itmid-iwinh:itmid+iwinh),x2(itmid-iwinh:itmid+iwinh),'Color',[0.5,0,0.5])
hold off
axis tight
legend('x1','x2')
subplot(4,1,4)
hold on
plot(t(itran-iwinh:itran+iwinh),x1(itran-iwinh:itran+iwinh),'Color',[0,0.5,0])
plot(t(itran-iwinh:itran+iwinh),x2(itran-iwinh:itran+iwinh),'Color',[0.5,0,0.5])
hold off
axis tight
xlabel('Time [s]')
fname = ['un_',num2str(f0),'-',num2str(f0-f_diff),'Hz_',num2str(Tdur),'s.png']
saveas(gcf, fname)
% end of file