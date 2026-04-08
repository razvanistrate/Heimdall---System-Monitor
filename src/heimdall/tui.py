import asyncio
from psutil._common import bytes2human
from textual.binding import Binding
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.containers import ScrollableContainer 
from textual.reactive import reactive
from textual.widgets import Static
from textual.widgets import Header, Footer

from heimdall.cpu import get_cpu 
from heimdall.memory import get_memory 
from heimdall.process import get_processes 
from heimdall.network import get_network
from heimdall.disk import get_disks


##-HeimdallAPP & Panel Styles-## 

#class Panel(Static):
#    DEFAULT_CSS = """
#            Screen {
#                layout: vertical
#           }
#            Horizontal {
#                height: 1fr;
#                align: center middle;
#            }
#            Vertical {
#                height: auto;
#                width: 50;
#                align: center middle;
#            }
#            Panel {
#                border: round white;
#                padding: 1;
#                margin: 1;
#                content-align: center middle;
#                width: 25;
#                text-align: left;
#
#            }
#        
#        """


class HeimdallApp(App):
    BINDINGS = [Binding(key="q", action="quit", description="Quit")]
    DEFAULT_CSS = """
        Screen {
            layout: vertical;
        }
        Horizontal {
            height: 12;
            width: 100%;
        }
        
        #cpu, #network, #memory, #disk {
            width: 1fr;
            height: 100%;
            border: round white;
            padding: 1 2;
        }

        #processes_scroll {
            height: 1fr;
            width: 100%;
            border: round white;
            padding: 1;
            margin: 1;
        }
        #processes {
            height: auto;
            width: 1fr;        
        }

        ScrollableContainer {
            height: 1fr;
            width: 100%;
            border: round white;
            padding: 1;
            margin: 1;
        }

        Footer {
            height: 3;
            width: 100%;
            border: round white;
            padding: 1;
            content-align: center middle;
        } 
"""

    ##-Data's of HeimdallAPP-##

    TITLE = "HEIMDALL"
    SUB_TITLE = "System Monitor"

    memory_text: str = reactive("")
    cpu_text: str = reactive("")
    processes_text: str = reactive("")
    disk_text: str = reactive("") 

    def compose(self) -> ComposeResult:
        yield Header()

        yield Horizontal(
            Static("", id="cpu"), 
            Static("", id="memory"),
            Static("", id="network"),
            Static("", id="disk")
        )

        yield ScrollableContainer(
            Static("", id="processes"),
            id="processes_scroll"
        )

        yield Footer(
            id="footer"
        )

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

        disks = get_disks()


        disk_lines = []
        for d in disks:
            disk_lines.append(
                f"Mountpoint - {d["mountpoint"]}\n"
                f"Used - {d["used_gb"]:.1f} / {d["total_gb"]:.1f} GB\n"
                f"Percent - {d["percent"]:.1f}%"
            )
        disk_text = '\n'.join(disk_lines)

        ##-Panel description-##

        cpu_panel = self.query_one("#cpu", Static)
        memory_panel = self.query_one("#memory", Static)
        processes_panel = self.query_one('#processes', Static)
        processes_scroll = self.query_one('#processes_scroll', ScrollableContainer)
        network_panel = self.query_one('#network', Static)
        disk_panel = self.query_one('#disk', Static)

        cpu_panel.border_title = "[bold cyan] CPU [/bold cyan]"
        memory_panel.border_title = "[bold cyan] Memory [/bold cyan]"
        processes_scroll.border_title = "[bold cyan] Processes [/bold cyan]"
        network_panel.border_title = "[bold cyan] Network [/bold cyan]"
        disk_panel.border_title = "[bold cyan] Disk [/bold cyan]"
        
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

        disk_panel.update(disk_text)
        


def run() -> None:
    app = HeimdallApp()
    app.run()
