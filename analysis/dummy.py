import numpy as np 

def get_samples(means, std_devs, sample_width, samples_per_mean):
    z = []
    shp = (samples_per_mean, sample_width)
    for m,s in zip(means, std_devs):
        x = np.random.normal(m, s, shp)
        y = np.hstack((m * np.ones(samples_per_mean)[:,None], x)) 
        z.append(y)
    return np.concatenate(z, axis=0)

