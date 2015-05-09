# Action selection system
# Author: Christos Kaplanis


from brian2 import *

# Variables
N = 4
taum = 10*ms
taupre = 20*ms
taupost = taupre
tauc = 20*ms # Izhikevich paper 1s
tauDop = 20*ms #  Izhikevich paper 200ms
Ee = 0*mV
vt = -54*mV
vr = -60*mV
El = -74*mV
taue = 5*ms
F = 15*Hz
gmax = 1

dApre = 1 # 0.01
dApost = -dApre * taupre / taupost *1.05 #* 1.05
dApost *= gmax
dApre *= gmax

sim_time = 1000 * ms
frame_length = 10 * ms

dopBoost = 0.5

# Neuron equations
eqs_neurons = '''
dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

# Poisson input
input = PoissonGroup(N, rates=F)

# Action selection neurons
neurons = NeuronGroup(N, eqs_neurons, threshold='v>vt', reset='v = vr')

# Synapses
S = Synapses(input, neurons,
             '''
                dApre/dt = -Apre / taupre : 1 
                dApost/dt = -Apost / taupost : 1 
                dDop/dt = -Dop / tauDop : 1 
                dc/dt = -c / tauc : 1
                dw/dt = c*Dop : 1
             ''',
             pre='''w = clip(w, 0, gmax)
                    ge += w
                    Apre += dApre
                    c = c + Apost''',
             post='''w = clip(w, 0, gmax)
                     Apost += dApost
                     c = c + Apre''',
             connect=True,
             )
#S.w = 0.5 * gmax
S.w = 'rand() * gmax'
S.c = 'rand() * gmax'

#Subgroups
neuron0=neurons[0:1]
neuron1=neurons[1:2]
neuron2=neurons[2:3]
neuron3=neurons[3:4]

# Monitors
mon = StateMonitor(S, ('w', 'Dop', 'c'), record=True)
w0_mon = StateMonitor(S, 'w', S[:,0])
w1_mon = StateMonitor(S, 'w', S[:,1])
w2_mon = StateMonitor(S, 'w', S[:,2])
w3_mon = StateMonitor(S, 'w', S[:,3])
s_mon = SpikeMonitor(neurons)
r0_mon = PopulationRateMonitor(neuron0)
r1_mon = PopulationRateMonitor(neuron1)
r2_mon = PopulationRateMonitor(neuron2)
r3_mon = PopulationRateMonitor(neuron3)

#run(sim_time, report='text')

# Simulation loop
num_spikes = 0
for i in range(sim_time / frame_length):
    run(frame_length, report='text')
    
    if s_mon.num_spikes > num_spikes:
        if 0 in s_mon.i[range(num_spikes, s_mon.num_spikes)]:
            S.Dop += dopBoost
        num_spikes = s_mon.num_spikes

print r3_mon.rate/Hz

# Plots
figure(1)
subplot(331)
plot(S.w / gmax, '.k')
ylabel('Weight / gmax')
xlabel('Synapse index')
subplot(332)
plot(w0_mon.t/second, w0_mon.w.T)
title('Synapses to Neuron 0')
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(333)
plot(w1_mon.t/second, w1_mon.w.T)
title('Synapses to Neuron 1')
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(334)
plot(w2_mon.t/second, w2_mon.w.T)
title('Synapses to Neuron 2')
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(335)
plot(w3_mon.t/second, w3_mon.w.T)
title('Synapses to Neuron 3')
xlabel('Time (s)')
ylabel('Weight / gmax')
subplot(336)
plot(s_mon.t/second, s_mon.i, '.')
xlabel('Time (s)')
ylabel('Neuron number')
subplot(337)
plot(mon.t/second, mon.Dop[0])
ylabel('Dopamine')
subplot(338)
plot(mon.t/second, mon.c[0])
ylabel('c')
subplot(339)
plot(r0_mon.t/second, r0_mon.rate/Hz)
xlabel('Time/s')
ylabel('Firing rate / Hz')
tight_layout()

figure(2)
subplot(221)
plot(r0_mon.t/second, r0_mon.rate/Hz)
title('Neuron 0 firing rate')
xlabel('Time/s')
ylabel('Firing rate / Hz')
subplot(222)
plot(r1_mon.t/second, r1_mon.rate/Hz)
title('Neuron 1 firing rate')
xlabel('Time/s')
ylabel('Firing rate / Hz')
subplot(223)
plot(r2_mon.t/second, r2_mon.rate/Hz)
title('Neuron 2 firing rate')
xlabel('Time/s')
ylabel('Firing rate / Hz')
subplot(224)
plot(r3_mon.t/second, r3_mon.rate/Hz)
title('Neuron 3 firing rate')
xlabel('Time/s')
ylabel('Firing rate / Hz')

show()