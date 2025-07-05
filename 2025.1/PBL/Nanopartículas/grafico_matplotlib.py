import matplotlib.pyplot as plt

wavelength = []
absorbance = []

file_name = ['sintese1.txt', 'sintese2.txt']

for name in file_name:
    with open(f'{name}', 'r') as file:
        W = []
        A = []

        for line in file:
            w, a = line.strip().split(',')
            W.append(float(w))
            A.append(float(a))
        
        wavelength.append(W)
        absorbance.append(A)
        del W, A


# COMPRIMENTO DE ONDA MÁXIMO
max_w = wavelength[0][absorbance[0].index(max(absorbance[0]))], wavelength[1][absorbance[1].index(max(absorbance[0]))]
print(f'W_máx_A_1 = {max_w[0]} \nW_máx_A_2 = {max_w[1]}')

#FWMH DA AMOSTRA 1
# Como é conhecido que absorbance[0] é a máxima absorção para wavelength igual a 200 nm, então wavelength[0] = 0
index2_a1 = 0
for i in absorbance[0]:
    if index2_a1 == 0: # Pega o primeiro valor imediatamente menor que 0.25 
        if i <= 0.25:
            index2_a1 = absorbance[0].index(i)

FWMH_A1 = wavelength[0][index2_a1] - 0
print(f'FWMH_A1 = {FWMH_A1}')

# FWMH DA AMOSTRA 2
index1_a2 = 0
index2_a2 = 0
for i in absorbance[1]:
    if i == 0.25 and index1_a2 == 0:
        index1_a2 = absorbance[1].index(i)
    elif 0.25 <= i <= 0.26 and index1_a2 != 0:
        index2_a2 = absorbance[1].index(i)

FWMH_A2 = wavelength[0][index2_a2] - wavelength[0][index1_a2]
print(f'FWMH_A2 = {FWMH_A2}')


plt.figure(figsize=(10, 6))
plt.title('Espectro de Absorbância UV-Vis das Nanopartículas de Prata')
plt.xlabel('Comprimento de Onda (nm)')
plt.ylabel('Absorbância (a.u.)')
plt.grid(True)

color = ['blue', 'red']

for i in range(len(wavelength)):
    plt.plot(wavelength[i], absorbance[i], color=color[i], label=f'Síntese {i+1}')
plt.legend()
plt.show()