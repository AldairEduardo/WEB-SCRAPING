import asyncio
from playwright.async_api import async_playwright

async def eliminar_bloqueadores(page):
    try:
        await page.evaluate('''() => {
            const bloqueadores = document.querySelectorAll('svg[fill="#888888"], #dismiss-button');
            bloqueadores.forEach(el => el.remove());
        }''')
        print("Elementos bloqueadores eliminados.")
    except Exception as e:
        print(f"No se encontraron elementos bloqueadores: {e}")

async def buscar_dni():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Cambia a headless=True si no necesitas depuración
        page = await browser.new_page()

        await page.goto('https://eldni.com/pe/buscar-por-dni')

        dni = input("Ingrese el DNI que desea buscar: ")

        if not dni.isdigit() or len(dni) != 8:
            print("El DNI debe tener 8 dígitos numéricos. Intente de nuevo.")
            return

        print(f"Buscando datos para el DNI: {dni}")
        await page.fill('#dni', dni)

        await eliminar_bloqueadores(page)

        try:
            await page.wait_for_selector('#btn-buscar-por-dni', state='visible', timeout=10000)
            await page.click('#btn-buscar-por-dni')
            print("Clic en el botón realizado.")
        except Exception as e:
            print(f"No se pudo hacer clic en el botón: {e}")
            return

        try:
            print("Esperando resultados...")
            await page.wait_for_selector('#completos', state='visible', timeout=15000)
            resultado = await page.get_attribute('#completos', 'value')
            print("Resultados encontrados:")
            print(resultado)
            
        except Exception as e:
            print("No se encontraron resultados")

        try:
            screenshot_path = "error_screenshot.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Se tomó una captura de pantalla para depuración: {screenshot_path}")
        except Exception as e:
            print(f"No se pudo tomar la captura de pantalla: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(buscar_dni())