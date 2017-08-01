import numpy as np
from results import Results, Trial, Series
import plot

import matplotlib.pyplot as plt
plt.style.use('ggplot')


experiment = "experiment_mnist_coloured.pickle"
res = Results.load(experiment)


### Figure 1 ###

trials = ['mnist_colored_vae_joint', 'mnist_colored_vae_translate',
          'mnist_colored_vae_cnn', 'mnist_colored_vae_cnn_color']
labels = ['Joint Bound', 'Translation Bound', 'CNN Bound', 'CNN Color Bound']

plt.figure(figsize=(12,9))

for i,t in enumerate(trials):
    if res.contains(t):
        run = res.get(t)
        steps, series = run.get_series('test_lower_bound')
        plt.plot(steps, series, label=labels[i], linewidth=2)

plt.axis([0,5000,-700,-550])
plt.legend(loc='lower right', fontsize=18)
plt.xlabel('Training Steps')
plt.ylabel('Log-Likelihood Lower Bound')
plt.title('Coloured MNIST Test Performance')

plt.savefig('../plots/coloured_mnist_test.png')
plt.close('all')



### Figure 2 ###

trials = ['mnist_colored_vae_joint', 'mnist_colored_vae_translate']
labels = ['Coloured Joint Bound', 'Coloured Translation Bound']

n_images = 18
time_steps = [500, 1000]

for time_step in time_steps:
    
    print("Timestep: ", time_step, flush=True)

    for i,t in enumerate(trials):
        print("At trial: ", t, flush=True)

        if not res.contains(t):
            continue

        run = res.get(t)

        x1b, rx2_1 = run.get_series('x2_1', i=time_step)

        images = np.concatenate((x1b[0:n_images],rx2_1[0:n_images]), axis=0)
        images = np.reshape(images, [-1,28,28,3])

        plot.plot_images(images, 6, 6, '../plots/'+labels[i]+'_reconstruct_from_x1_'+str(time_step)+'.png')

        #----

        x2b, rx1_2 = run.get_series('x1_2', i=time_step)

        images = np.concatenate((x2b[0:n_images],rx1_2[0:n_images]), axis=0)
        images = np.reshape(images, [-1,28,28,3])

        plot.plot_images(images, 6, 6, '../plots/'+labels[i]+'_reconstruct_from_x2_'+str(time_step)+'.png')
