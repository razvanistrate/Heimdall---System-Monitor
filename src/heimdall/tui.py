import asyncio
from psutil._common import bytes2human

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal
#from textual.containers import Vertical
from textual.containers import ScrollableContainer 
from textual.reactive import reactive
from textual.widgets import Static
from textual.widgets import Button, Label
from textual.widgets import Header, Footer

from heimdall.cpu import get_cpu 
from heimdall.memory import get_memory 
from heimdall.process import get_processes 
from heimdall.network import get_network


##-HeimdallAPP & Panel Styles-## 

class Panel(Static):
    DEFAULT_CSS = """
            Screen {
                layout: vertical
            }
            Horizontal {
                height: 1fr;
                align: center middle;
            }
            Vertical {
                height: auto;
                align: center middle;
                width: 50;
            }
            Panel {
                border: round white;
                padding: 1;
                margin: 1;
                content-align: center middle;
                text-align: left;
                width: 25;

            }
        
        """


class HeimdallApp(App):
    DEFAULT_CSS = """
        Screen {
            layout: vertical;
        }
        
        #processes_scroll {
            height: 15;
            width: 1fr;
            border: round white;
            padding: 1;
            margin: 1;
             }
        #processes {
            height: auto;
            width: 1fr;
                
             }        
"""

    ##-Data's of HeimdallAPP-##

    theme= "nord"
    TITLE = "HEIMDALL"
    SUB_TITLE = "System Monitor"

    memory_text: str = reactive("")
    cpu_text: str = reactive("")
    processes_text: str = reactive("")
     

    def compose(self) -> ComposeResult:
        yield Header()

        yield Horizontal(
            Panel("", id="cpu"), 
            Panel("", id="memory"),
            Panel("", id="network")
        )

        yield ScrollableContainer(
            Static("", id="processes"),
            id="processes_scroll"
        )

        yield Horizontal(
            Button("Quit", id="quit")
        )

        yield Footer(
            id="footer"
        )


    def on_button_pressed(self, event: Button.Pressed) -> None:
            if event.button.id == "quit":
                self.exit()  

    async def on_mount(self) -> None:
        self.prev_network = None
        self.set_interval(1, self.refresh_data)

         


    def refresh_data(self) -> None:
        mem = get_memory()
        cpu = get_cpu()
        raw_processes = get_processes() or []
        processes = sorted([p for p in raw_processes if p is not None and len(p) > 0], key=lambda p: p[0], reverse=True)[:50]

        ##-Network Data-##

        network = get_network()

        if network is not None and self.prev_network is not None:

            upload_speed = network["sent"] - self.prev_network["sent"]
            download_speed = network["recv"] - self.prev_network["recv"]

        else:
            upload_speed = 0
            download_speed = 0    
        
        download_mb = download_speed / (1024 * 1024)
        upload_mb = upload_speed / (1024 * 1024)

        self.prev_network = network

        ##-Finish Network Data-##

        process_text = "\n".join(f"{pid:>5} {name}" for pid, name in processes)
        if network is None:
            network_text = "No network data available"
        else:
            network_text = (
                f"Interface: {network['name']}\n"
                f"Download: {download_mb:.2f} MB/s\n"
                f"Upload: {upload_mb:.2f} MB/s\n"
                f"Speed: {network['speed']:.2f} Mbps"
            )

        ##-Panel description-##

        cpu_panel = self.query_one("#cpu", Panel)
        memory_panel = self.query_one("#memory", Panel)
        processes_panel = self.query_one('#processes', Static)
        processes_scroll = self.query_one('#processes_scroll', ScrollableContainer)
        network_panel = self.query_one('#network', Panel)

        cpu_panel.border_title = "[bold cyan] CPU [/bold cyan]"
        memory_panel.border_title = "[bold cyan] Memory [/bold cyan]"
        processes_scroll.border_title = "[bold cyan] Processes [/bold cyan]"
        network_panel.border_title = "[bold cyan] Network [/bold cyan]"

        ##-Update Data Section-##

        cpu_panel.update(
            f"Name: {cpu['name']}\n"
            f"Cores: {cpu['cores']}\n"
            f"Threads: {cpu['threads']}"
        )

        memory_panel.update(
            f"Total: {mem['total_mb']:.0f} MB\n"
            f"Used:  {mem['used_mb']:.0f} MB\n"
            f"Percent: {mem['used_percent']:.2f}%"
        )

        processes_panel.update(process_text)

        network_panel.update(network_text)


        


def run() -> None:
    app = HeimdallApp()
    app.run()
