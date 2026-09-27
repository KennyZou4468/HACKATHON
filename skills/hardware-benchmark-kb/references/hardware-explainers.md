# Hardware terms in plain language

Use this reference for a user asking what a CPU, GPU, RAM, or storage specification means. These are stable concepts: answer without web search or Shopee unless the user asks about a particular current model, product, price, benchmark, driver, or compatibility claim.

## Response style

- Lead with one plain-language answer connected to the user's stated workload, if known.
- Explain only the term asked about; normally use 2–4 short bullets. Define an abbreviation on first use.
- Use careful phrasing: a higher specification can provide more headroom, but does not by itself guarantee FPS, compile time, cooling, battery life, upgradeability, or compatibility.
- If the listing does not explicitly state a detail, call it unknown. Do not guess TGP, RAM channels, SSD slots, or upgrade paths.

## CPU

- **CPU / processor**: the general-purpose “brain”; it schedules programs, browser tabs, code builds, and game logic.
- **Core**: one worker inside the CPU. More cores can handle more separate heavy jobs at once; it does not make every single task proportionally faster.
- **Thread**: a work queue a core can handle. Many modern cores expose two threads, so `8 cores / 16 threads` does not mean 16 physical cores.
- **P-core / E-core**: on some Intel CPUs, P-cores handle demanding foreground work; E-cores handle efficient/background work. Report both only when the exact CPU specification is sourced.
- **Clock / boost clock (GHz)**: how quickly a core can cycle. It is not a standalone speed score; CPU design, power limit, and cooling also matter.
- **Cache**: small, very fast memory inside or near the CPU. It reduces waits for frequently used data, but cache size alone does not predict game FPS.
- **TDP / processor power**: a power/thermal design reference, not fixed electricity use or fixed performance. A laptop maker's allowed power and cooling change sustained results.

## GPU

- **GPU / graphics card**: the processor mainly responsible for 3D graphics and some parallel compute work.
- **Integrated GPU**: built into the CPU and shares system RAM; good enough for display/basic graphics, but is not interchangeable with a dedicated GPU.
- **Dedicated GPU**: a separate graphics processor with its own VRAM; the exact model, power limit, and cooling still matter.
- **VRAM / graphics memory**: memory reserved for textures, game assets, and GPU workloads. More VRAM can avoid memory pressure in some workloads, but does not alone prove a game setting or FPS target.
- **TGP / GPU power limit (laptop)**: the power the laptop lets the GPU use. Same `Laptop GPU` name can perform differently at different TGP and cooling designs.
- **Board power / TDP (desktop)**: desktop-card power reference; do not call it laptop TGP and do not equate it to a laptop GPU of the same name.
- **Ray tracing**: a graphics technique for more realistic lighting/reflections; it usually increases GPU load.
- **DLSS / FSR / XeSS / frame generation**: upscaling or generated-frame features. They are settings, not base GPU performance; always state whether a benchmark has them enabled.

## RAM / system memory

- **RAM / memory**: the desk space for programs currently open. Too little memory can force the system to use slower storage as overflow, causing stutter or slow switching.
- **Capacity (GB)**: how much can stay open at once. It is different from SSD storage capacity.
- **DDR4 / DDR5**: memory generations. The generation alone does not establish total system speed; capacity, speed, channel layout, and workload matter.
- **MT/s / memory speed**: transfer rate. Higher can help some workloads, but it is not a direct FPS or multitasking guarantee.
- **Single-channel / dual-channel**: one versus two active memory paths. It matters especially to integrated graphics, but must be explicitly sourced; two physical modules alone do not prove a laptop's operating mode.
- **Soldered RAM / slots**: soldered RAM is fixed to the board; slots may permit changes, but a listing must explicitly confirm capacity and support before claiming an upgrade path.

## Storage

- **SSD**: persistent storage for Windows, apps, games, and files. It keeps data after shutdown; it is not RAM.
- **Capacity (GB/TB)**: how much can be stored. Usable space is lower than the label after formatting and system files.
- **NVMe / PCIe SSD**: a common fast SSD connection. **SATA SSD** is another SSD connection and is generally slower in large transfers, but both can feel responsive for ordinary tasks.
- **Read/write speed**: how fast large data can be read or saved in a specified test; it does not by itself prove game FPS or every app's loading time.
- **PCIe generation**: connection-generation capability. The drive, slot, heat management, and workload determine actual behavior.
- **HDD**: mechanical storage; usually larger/cheaper per GB but slower and less impact-resistant than SSDs.
- **M.2 slot / extra slot**: a physical expansion location. Never promise a second slot or upgrade support unless the exact product documentation confirms it.
