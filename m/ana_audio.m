clear all;
close all;
clc
set(0,'defaultAxesFontSize',18)

%% ファイル名などの設定
fname = '/MATLAB Drive/MobileSensorData/sensorlog_20yymmdd_HHMMSS.m4a'; %「パスをコピー」から貼り付け
T_win = 0.1;

%% 音声信号の読み取り
[x, Fs] = audioread(fname);
xL = x(:,1);
%xR = x(:,2);
nd = length(xL);
dt = 1/Fs;
t = [0:dt:nd*dt-dt];
itmid = round(nd/2);
iwinh = round(T_win*Fs/2);

%% 解析
%[pperi, fperi] = periodogram(xL(itmid-iwinh:itmid+iwinh),[],Fs,Fs);
Y = fft(x)/nd;
pperi = real(Y.*conj(Y));
fperi = linspace(1/max(t),Fs,length(pperi));
[pxx, f] = pwelch(xL(itmid-iwinh:itmid+iwinh), [], 0, [], Fs);
[spec,freq,time] = spectrogram(xL,2048,1023,1024,Fs);
pt = abs(spec).^2;
pt_db = 10*log10(pt);

%% 描画(1): 時間波形
figure(1)
subplot(2,1,1)
plot(t,xL,'b-')
hold on
plot(t(itmid-iwinh:itmid+iwinh),xL(itmid-iwinh:itmid+iwinh),'r-')
subplot(2,1,2)
plot(t(itmid-iwinh:itmid+iwinh),xL(itmid-iwinh:itmid+iwinh),'r-')
axis tight
xlabel('Time [s]')
ylabel('Amplitude [V]')
saveas(gcf,[fname,'_xt.png'])

%% 描画(2): ピリオドグラム
figure(2)
plot(fperi, pperi, 'r-', 'LineWidth',2)
%xscale log
xlim([150, 250]) %適宜調整すること．
ylabel('Power Spectral Density [V^2/Hz]')
xlabel('Frequency [Hz]')
grid on
saveas(gcf,[fname,'_peri.png'])

%% 描画(3): Welch法にもとづくパワースペクトル
figure(3)
plot(f, pxx, 'r-', 'LineWidth',2)
xscale log
ylabel('Power Spectral Density [V^2/Hz]')
xlabel('Frequency [Hz]')
grid on
saveas(gcf,[fname,'_psd.png'])

%% 描画(4): 短時間フーリエ変換・スペクトログラム
figure(4)
%s = surface(time,freq,pt);
s = surface(time,freq,pt_db);
s.EdgeColor = 'none';
s.FaceAlpha = 0.5;
grid on
view(2), axis tight
colorbar;
yscale log
xlabel('Time [s]')
ylabel('Frequency [Hz]')
saveas(gcf,[fname,'_spectro.png'])
%% end of file