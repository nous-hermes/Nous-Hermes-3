# Nous Hermes 3 — User Guide and Project Documentation

Nous Hermes 3 desktop client for Windows (.exe) & macOS (.dmg): local AI, function calling, JSON output, 128K context, roleplay, coding, and full setup guide.

---

<div align="center">
  <a href="../../releases/latest">
    <img width="1200" alt="Nous Hermes 3." src="assets/2ah3vafmjs.jpg" />
  </a>
</div>

---

## Why Choose Nous Hermes 3 (Pros and Advantages)

**Nous Hermes 3** is a series of fine-tuned language models from **Nous Research**, built on the **Llama 3.1** architecture and designed for agentic workflows, precise instruction following, roleplay, and deep context handling.

### Key Advantages of the Model:

* **Neutral Alignment and High Steerability:** The model is tuned to follow the `system prompt` faithfully without excessive refusals common in base instruction models, making it well-suited for custom pipelines and complex personas.
* **Reliable Function Calling and Structured Output (JSON / XML):** Hermes 3 is trained to call tools accurately and return valid data structures (such as JSON matching a requested schema), which is critical for AI agents and automation.
* **Large Context Window (up to 128K tokens):** Support for long context allows retaining large volumes of information, documentation, and multi-turn conversation history.
* **Improved Multi-Turn Conversations and Context Retention:** The model maintains coherence, details, and assigned style across long dialogues and many steps.
* **Strong Roleplay and Inner Monologue Capabilities:** Well-suited for creative tasks, scenario writing, characters, and step-by-step reasoning ("inner monologue").
* **Enhanced Code Generation and Reasoning:** Compared to earlier versions in the Hermes lineup, coding, analysis, and logical problem-solving capabilities are strengthened.
* **Multiple Model Sizes for Different Tasks and Hardware:** The lineup includes variants at different scales (including compact versions for local execution and larger models such as 70B and 405B for high accuracy), letting you balance speed, VRAM requirements, and response quality.
* **Local Execution and API Cost Savings:** When run locally (for example, via Ollama, llama.cpp, LM Studio, or a desktop client), there are no per-token API fees and your data stays on your machine.

---

## Desktop Client Installation (.exe / .dmg)

### Installing on Windows (`.exe`)

1. Download the latest Windows installation file from the repository [releases](../../releases) page.
2. Double-click the downloaded file (for example, `Hermes-Desktop-x64.exe` or the Windows installer package) to run it.
3. If **Windows SmartScreen** displays a warning about an unrecognized publisher, click **More info** -> **Run anyway** (and approve administrator privileges in the UAC prompt if requested).
4. Follow the setup wizard instructions: choose the installation directory (if available) and wait for file copying to finish.
5. Launch the application from the Start menu or desktop shortcut after installation completes.

### Installing on macOS (`.dmg`)

1. Download the **`.dmg`** image file for your architecture (Apple Silicon `arm64` or compatible build) from the [releases](../../releases) page.
2. Double-click the downloaded `.dmg` file to mount the virtual disk.
3. In the opened window, drag and drop the **Hermes** app icon into the **Applications** folder.
4. Eject the mounted disk image from the desktop or Finder.
5. Open the app from the **Applications** folder.
   * *If macOS blocks launch due to security policy ("developer cannot be verified"):* open **System Settings -> Privacy & Security**, scroll to the message about the blocked app, click **Open Anyway**, and confirm your choice.

---

## Complete Feature Overview

Below is the full lifecycle of using the client and the **Nous Hermes 3** model—from first launch to exporting results and automating workflows.

### Stage 1. First Launch and Initial Setup (Onboarding)
* **Workspace Initialization:** On first launch, the app creates local directories for configuration, chat history, and cache.
* **Backend / Mode Selection:** Connect to a local inference engine (such as Ollama, LM Studio, llama.cpp, or a built-in runtime) or to a remote API-compatible endpoint (`OpenAI-compatible` / local server).
* **Model Selection and Download:** Choose the desired Hermes 3 variant (for example, a compact model for fast local responses or a larger model for complex reasoning and coding).
* **Interface Customization:** Configure the theme (light/dark), UI language, keyboard shortcuts, and system tray / background minimization behavior.

### Stage 2. Session and Conversation Management
* **Chat Creation and Organization:** Create new chats, rename conversations, pin important sessions, search history, and delete outdated threads.
* **System Instructions (System Prompts):** Define global or per-chat system rules (assistant role, response format, constraints, communication tone).
* **Multi-Turn Context:** Maintain a message chain within the model's context window, with options to clear context or start a new branch without losing settings.
* **Editing and Regeneration:** Edit a sent message and regenerate the model's response with updated generation parameters.

### Stage 3. Fine-Tuning Generation Parameters
* **Temperature:** Adjust the balance between precision/determinism and creativity.
* **Top-P / Top-K and Repetition Penalties:** Control vocabulary diversity and prevent repetitive loops in generated text.
* **Max Tokens / Context Length:** Limit maximum output length and manage context size according to available memory (VRAM / RAM).
* **Parameter Presets:** Quickly switch between ready-made profiles (for example, *Code & Analysis*, *Creative / Roleplay*, *Precise Assistant*).

### Stage 4. Working with Code, Text, and Structured Data
* **Code Generation, Refactoring, and Debugging:** Write scripts, explain errors, spot vulnerabilities, and optimize algorithms with syntax highlighting and one-click code copying.
* **Structured Output (JSON / Schemas):** Obtain outputs in strict formats for downstream programmatic processing or integration with other services.
* **Roleplay and Scenario Modes:** Support complex characters, world rules, and sequential reasoning.

### Stage 5. Tools (Function Calling) and Agentic Workflows
* **Attaching Tools:** Define available functions/tools that the model can invoke when needed.
* **Tool Execution Loop:** The model outputs a structured function call request with arguments, the application executes the action, and the result is fed back into the context to produce the final answer.

### Stage 6. Data Storage, Export, and Updates
* **Local History Storage:** Conversations and settings are stored locally on the user's device (when running locally, traffic is not sent to third-party cloud servers).
* **Export and Backup:** Save chats and configurations in convenient formats (such as Markdown / JSON) for migration or archival.
* **Client and Model Updates:** Check for new desktop client versions (including built-in updates / downloading new releases) and update model weights or quantizations.


---

## License and Links

* **Nous Hermes 3 Models:** Developed by **Nous Research** on the Meta Llama 3.1 architecture; when using model weights, follow the applicable license terms (including the Llama 3.1 Community License).
* **Repository License:** Specify your chosen project license (for example, `MIT` or `Apache-2.0`) in the `LICENSE` file.


