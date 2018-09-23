This is my graduation thesis code repository.

AuthorEvaluation is a method aimed to quantify authors' contribution in a certain scientific area.

I built a author citation network, which is a directed graph G, based on the paper citation relationship. In the network G, each node represents an author, each directed edge represents a citation relationship. For example, if author A has cited author B in one of his/her paper, then there should be a egde from A to B on G.

In order to give every author a vector representation, I used node2vec[1] alogorithm to train graph G. The outcome of training is stored in folder /emb.
[1] node2vec is a network embedding method developped by A. Grover and J. Leskovec, you can read their paper "node2vec: Scalable Feature Learning for Networks" on this site: https://arxiv.org/abs/1607.00653 .

