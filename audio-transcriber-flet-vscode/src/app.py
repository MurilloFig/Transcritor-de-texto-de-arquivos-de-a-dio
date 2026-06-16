\
import flet as ft
from pathlib import Path
from transcriber import AudioTranscriber


def main(page: ft.Page):
    page.title = "Audio Transcriber PT/EN"
    page.window_width = 980
    page.window_height = 760
    page.window_min_width = 820
    page.window_min_height = 640
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 24

    transcriber = AudioTranscriber()
    selected_file_path = ft.Text(
        value="Nenhum arquivo selecionado.",
        size=13,
        color=ft.Colors.GREY_400,
        selectable=True
    )

    status_text = ft.Text(
        value="Selecione um áudio para iniciar.",
        size=14,
        color=ft.Colors.BLUE_200
    )

    result_text = ft.TextField(
        label="Transcrição",
        multiline=True,
        min_lines=14,
        max_lines=20,
        read_only=True,
        border_radius=12,
        text_size=14
    )

    metadata_text = ft.Text(
        value="",
        size=13,
        color=ft.Colors.GREY_300,
        selectable=True
    )

    language_dropdown = ft.Dropdown(
        label="Idioma",
        value="auto",
        width=240,
        options=[
            ft.dropdown.Option("auto", "Detectar automaticamente"),
            ft.dropdown.Option("pt", "Português"),
            ft.dropdown.Option("en", "Inglês"),
        ],
    )

    progress_ring = ft.ProgressRing(visible=False)

    selected_path = {"value": None}

    def set_busy(is_busy: bool):
        progress_ring.visible = is_busy
        transcribe_button.disabled = is_busy
        pick_button.disabled = is_busy
        language_dropdown.disabled = is_busy
        page.update()

    def on_file_selected(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        selected_path["value"] = e.files[0].path
        selected_file_path.value = selected_path["value"]
        status_text.value = "Arquivo selecionado. Clique em Transcrever."
        status_text.color = ft.Colors.BLUE_200
        page.update()

    def transcribe_click(e):
        if not selected_path["value"]:
            status_text.value = "Selecione um arquivo de áudio primeiro."
            status_text.color = ft.Colors.RED_300
            page.update()
            return

        set_busy(True)
        status_text.value = "Transcrevendo áudio. Aguarde a finalização do processamento."
        status_text.color = ft.Colors.AMBER_200
        result_text.value = ""
        metadata_text.value = ""
        page.update()

        try:
            result = transcriber.transcribe(
                file_path=selected_path["value"],
                language=language_dropdown.value
            )

            result_text.value = result["text"]

            metadata_text.value = (
                f"Idioma detectado: {result['detected_language']} | "
                f"Confiança: {result['language_probability']} | "
                f"Duração: {result['duration']}s | "
                f"Arquivo salvo em: {result['output_file']}"
            )

            status_text.value = "Transcrição concluída com sucesso."
            status_text.color = ft.Colors.GREEN_300

        except Exception as error:
            status_text.value = f"Erro: {error}"
            status_text.color = ft.Colors.RED_300

        finally:
            set_busy(False)

    def clear_click(e):
        selected_path["value"] = None
        selected_file_path.value = "Nenhum arquivo selecionado."
        status_text.value = "Selecione um áudio para iniciar."
        status_text.color = ft.Colors.BLUE_200
        result_text.value = ""
        metadata_text.value = ""
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    pick_button = ft.ElevatedButton(
        text="Selecionar áudio",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["mp3", "wav", "m4a", "ogg", "flac", "mp4", "webm"]
        )
    )

    transcribe_button = ft.FilledButton(
        text="Transcrever",
        icon=ft.Icons.TRANSCRIBE,
        on_click=transcribe_click
    )

    clear_button = ft.OutlinedButton(
        text="Limpar",
        icon=ft.Icons.DELETE_OUTLINE,
        on_click=clear_click
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.GRAPHIC_EQ, size=38, color=ft.Colors.BLUE_300),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Audio Transcriber PT/EN",
                                        size=28,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        "Transcreva áudios em português e inglês usando Whisper.",
                                        size=14,
                                        color=ft.Colors.GREY_300
                                    )
                                ],
                                spacing=2
                            )
                        ],
                        spacing=12
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Arquivo de áudio", size=16, weight=ft.FontWeight.BOLD),
                                selected_file_path,
                                ft.Row(
                                    controls=[
                                        pick_button,
                                        language_dropdown,
                                        transcribe_button,
                                        clear_button,
                                        progress_ring
                                    ],
                                    spacing=12,
                                    wrap=True
                                ),
                                status_text
                            ],
                            spacing=12
                        ),
                        padding=18,
                        border_radius=16,
                        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE)
                    ),
                    result_text,
                    metadata_text,
                    ft.Text(
                        "Dica: para melhor qualidade, use áudio limpo, sem muito ruído e com fala clara.",
                        size=12,
                        color=ft.Colors.GREY_500
                    )
                ],
                spacing=18
            ),
            expand=True
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
