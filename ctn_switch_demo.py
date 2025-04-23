# ctn_switch_demo.py  – NumPy only, runs in <5 s on a laptop
import numpy as np, matplotlib.pyplot as plt
n, N = 6, 3000                      # 6 values per axis, 3k samples
A, B  = np.random.randint(0, n, N), np.random.randint(0, n, N)
one   = lambda idx: np.eye(n)[idx]
XA, XB = one(A), one(B)
Xint   = (XA[:,:,None]*XB[:,None,:]).reshape(N, n*n)     # cross block
X      = np.hstack([XA, XB, Xint])                       # Φ(x)
y      = (((A+B) % n)==0).astype(float).reshape(-1,1)    # needs mixing

W = np.zeros((X.shape[1],1))
W[:n]       = 0.01*np.random.randn(n,1)                  # axis weights
W[n:2*n]    = 0.01*np.random.randn(n,1)
sig = lambda z: 1/(1+np.exp(-z))

lr, bs, ep = .5, 150, 80
acc, coupler = [], []
for _ in range(ep):
    for idx in np.array_split(np.random.permutation(N), N//bs):
        p = sig(X[idx]@W); W -= lr * X[idx].T@(p-y[idx])/bs
    acc.append(((sig(X@W)>0.5)==y).mean())
    coupler.append(np.linalg.norm(W[-n*n:]))             # cross-block norm

plt.plot(acc); plt.twinx().plot(coupler,'--')
plt.title('accuracy (solid) vs. coupler norm (dashed)')
plt.show()
