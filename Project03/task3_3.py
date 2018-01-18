import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# import data

x = np.loadtxt('data/data-dimred-X.csv', dtype=np.float, delimiter=',')
y = np.loadtxt('data/data-dimred-y.csv', dtype=np.float, delimiter=None)

x_classes = np.stack((x[:,y == 1],x[:,y == 2], x[:,y == 3]), axis=0)
n = 50

# -----------------------
# dim reduction using PCA
# -----------------------

# normalize mean
means = np.mean(x, axis=1)
x = (x.T - means).T

covariance = np.cov(x)
w, v = np.linalg.eigh(covariance)
pca_projected2d = np.dot(v[:,[-1,-2]].T, x)
pca_projected3d = np.dot(v[:,[-1,-2,-3]].T, x)

# ----------------------------------
# dim reduction using multiclass LDA
# ----------------------------------

# estimate class means and covariances
means = 1./n * np.sum(x_classes, axis=2, keepdims=True)
norm_classes = x_classes - means
covs = np.matmul(norm_classes, np.transpose(norm_classes,axes=(0,2,1)))

# within class scatter matrix
sw = np.sum(covs, axis=0)

# between class scatter matrix
sb = np.sum(np.matmul(means, np.transpose(means,axes=(0,2,1))),axis=0)

# calculate eigvecs of sw^(-1) * sb
w, v = np.linalg.eig(np.dot(np.linalg.inv(sw),sb))

# project data
sorted = np.argsort(w)
lda_projected2d = np.real(np.dot(v[:, sorted[[-1, -2]]].T, x))
lda_projected3d = np.real(np.dot(v[:, sorted[[-1, -2, -3]]].T, x))

# -------------
# visualization
# -------------

fig = plt.figure(figsize=(8,8))
# 2D PCA
ax = fig.add_subplot(221)
ax.scatter(*pca_projected2d)
ax.set_xlabel('$u_1$')
ax.set_ylabel('$u_2$')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_title("principal component analysis")

# 2D LDA
ax = fig.add_subplot(222)
ax.scatter(*lda_projected2d)
ax.set_xlabel('$u_1$')
ax.set_ylabel('$u_2$')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_title("linear discriminant analysis")

# 3D PCA
ax = fig.add_subplot(223,projection='3d')
ax.scatter(*pca_projected3d)
ax.set_xlabel('$u_1$')
ax.set_ylabel('$u_2$')
ax.set_zlabel('$u_3$')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

# 3D LDA
ax = fig.add_subplot(224,projection='3d')
ax.scatter(*lda_projected3d)
ax.set_xlabel('$u_1$')
ax.set_ylabel('$u_2$')
ax.set_zlabel('$u_3$')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

plt.tight_layout(w_pad=5)
plt.show()