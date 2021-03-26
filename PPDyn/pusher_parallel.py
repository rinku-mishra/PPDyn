from numba import jit, prange
import numpy as np

@jit(nopython=True, parallel=True)
def verlet(x,y,z,vx,vy,vz,ux,uy,uz,ax,ay,az,dt,Lx,Ly,Lz,N,KE):
    for i in prange(N):
        ux[i] = vx[i] + ax[i] * dt/2.0
        uy[i] = vy[i] + ay[i] * dt/2.0
        uz[i] = vz[i] + az[i] * dt/2.0
        x[i] = x[i] + ux[i] * dt
        y[i] = y[i] + uy[i] * dt
        z[i] = z[i] + uz[i] * dt
        x[i] = x[i] - (int(x[i]/Lx)) * 2.0 * Lx      # Periodic Boundary Condition
        y[i] = y[i] - (int(y[i]/Ly)) * 2.0 * Ly      # Periodic Boundary Condition
        z[i] = z[i] - (int(z[i]/Lz)) * 2.0 * Lz      # Periodic Boundary Condition

    for i in prange(N):
        ax[i] = 0.0
        ay[i] = 0.0
        az[i] = 0.0
        for j in range(N):
            if (i != j):
                xdiff = ( x[i]-x[j] ) - round((x[i]-x[j])/(2.0*Lx)) * 2.0*Lx
                ydiff = ( y[i]-y[j] ) - round((y[i]-y[j])/(2.0*Ly)) * 2.0*Ly
                zdiff = ( z[i]-z[j] ) - round((z[i]-z[j])/(2.0*Lz)) * 2.0*Lz
                r = np.sqrt(xdiff*xdiff + ydiff*ydiff + zdiff*zdiff)
                fx = xdiff/(r*r*r)
                fy = ydiff/(r*r*r)
                fz = zdiff/(r*r*r)
                ax[i] += fx
                ay[i] += fy
                az[i] += fz

    for i in prange(N):
        vx[i] = ux[i] + ax[i] * dt / 2.0
        vy[i] = uy[i] + ay[i] * dt / 2.0
        vz[i] = uz[i] + az[i] * dt / 2.0
        KE += ((vx[i]*vx[i]) + (vy[i]*vy[i]) + (vz[i]*vz[i]) ) / 2.0
    return x,y,z,vx,vy,vz,ux,uy,uz,ax,ay,az,KE
