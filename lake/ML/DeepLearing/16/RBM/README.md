code from: [https://github.com/echen/restricted-boltzmann-machines](https://github.com/echen/restricted-boltzmann-machines)

**It is strongly recommended to read the original author's README.md**

Add some content here for easy understanding

## Matrix interpretation

matrix[0][0] is useless

matrix[0][1:] is bias to computer hidden from data

matrix[1:][0] is bias to computer data from hidden

whether it is data or hidden, the first num is 1(used to multiply the bias)

matrix[1:][1:] is weight

## Update

pos_associations is the association learn from our training examples

neg_associations measures the association that the network itself generates

neg_associations like the **baseline** in reinforcement learning

## daydream function

It is essentially Gibbs sampling, continuous sampling hidden_states and visible_states num_samples times, and save result in samples
