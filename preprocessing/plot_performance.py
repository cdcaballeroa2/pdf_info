import numpy as np
import matplotlib.pyplot as plt


def resume_time(time_list, npage_list, error_cant):
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(f"Rendimiento / Archivos:{len(npage_list)} / Paginas:{sum(npage_list)} / "
                 f"Tiempo total: {int(sum(time_list))}s \n"
                 f"({round(sum(time_list) / len(npage_list), 4)} s/archivo) "
                 f"({round(sum(time_list) / sum(npage_list), 4)} s/pagina) "
                 f"({round(sum(npage_list) / len(npage_list), 1)} pags/archivo) \n"
                 f"Archivos con errores: {error_cant[0]} "
                 f"({round(error_cant[0] * 100 / sum(error_cant), 4)}%)")
    counts, bins = np.histogram(time_list, int(np.sqrt(len(time_list))))
    axs[0, 0].hist(time_list, bins=bins, orientation='horizontal')
    axs[0, 0].set_title("Tiempo por archivo")
    axs[0, 0].set_ylabel("Tiempo (s)")
    axs[0, 0].set_xlabel("Cantidad de archivos")

    axs[0, 1].scatter(npage_list, time_list)
    axs[0, 1].set_title("Tiempo segun cantidad de hojas")
    axs[0, 1].set_xlim(0, max(npage_list) + 1)
    axs[0, 1].set_xlabel("No. paginas")
    axs[0, 1].set_ylabel("Tiempo (s)")

    axs[1, 0].scatter(npage_list, time_list)
    axs[1, 0].set_title("Tiempo segun cantidad de hojas")
    axs[1, 0].set_xlim(0, 10)
    axs[1, 0].set_ylim(0, 30)
    axs[1, 0].set_xlabel("No. paginas")
    axs[1, 0].set_ylabel("Tiempo (s)")

    counts, bins2 = np.histogram(npage_list,
                                 int(np.sqrt(len(npage_list))))
    axs[1, 1].hist(npage_list, bins=bins2)
    axs[1, 1].set_xlim(0, max(npage_list) + 1)
    axs[1, 1].set_title("Hojas por archivo")
    axs[1, 1].set_xlabel("No. paginas")
    axs[1, 1].set_ylabel("Cantidad de archivos")

    axs[0, 0].grid(True)
    axs[0, 1].grid(True)
    axs[1, 0].grid(True)
    axs[1, 1].grid(True)

    fig.tight_layout()
    plt.savefig('/home/david/Documents/results_pdf/performance.png')
    plt.close()

def resume_quality(cat_totals, npage_list):
    fig, axs = plt.subplots(1, 3)

    fig.suptitle(f"Categoria / Archivos:{np.sum(cat_totals)} / Paginas:{sum(npage_list)} / "
                 f"({round(sum(npage_list) / len(npage_list), 1)} pags/archivo) \n")

    axs[0].pie(cat_totals,
               labels = [
                   'Blancos',
                   'Optimo',
                   'Medio',
                   'Baja',
                   'Revision',
                   'Digitalizado'],
               autopct = lambda data: f'{round(data/np.sum(cat_totals),2)}%')
    axs[0].set_title("Porcentaje de categorías (páginas)")

    axs[1].bar(cat_totals/np.sum(npage_list))
    axs[1].set_title("No. de hojas (por categoria) por archivo")
    axs[1].set_xlabel("Categoría")
    axs[1].set_ylabel("No. paginas")
    axs[1].grid(True)

    axs[2].pie(cat_totals[3:4],
               labels = [
                   'Baja',
                   'Revision'],
               autopct = lambda data: f'{round(data/np.sum(cat_totals[3:4]),2)}%')
    axs[2].set_title("Porcentaje de revision (calidad baja)")

    fig.tight_layout()
    plt.savefig('/home/david/Documents/results_pdf/categories.png')
    plt.close()