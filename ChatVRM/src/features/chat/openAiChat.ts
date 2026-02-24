import { Message } from "../messages/messages";
// === 引入我们刚才在 speakCharacter.ts 里写的打断函数 ===
import { interruptSpeakCharacter } from "../messages/speakCharacter"; 

const OLLAMA_MODEL = "qwen3:1.7b"; 

export async function getChatResponse(messages: Message[], apiKey: string) {
  // 普通请求也可以加上打断
  interruptSpeakCharacter(); 
  
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey || "ollama"}`,
  };

  try {
    const res = await fetch("http://localhost:11434/v1/chat/completions", {
      headers: headers,
      method: "POST",
      body: JSON.stringify({
        model: OLLAMA_MODEL,
        messages: messages,
        stream: false, // 非流式
      }),
    });

    if (!res.ok) throw new Error(`Ollama API Error: ${res.status}`);
    const data = await res.json();
    const message = data.choices[0]?.message?.content || "无回复";
    return { message: message };
  } catch (e) {
    console.error(e);
    return { message: "连接本地 Ollama 失败" };
  }
}

export async function getChatResponseStream(
  messages: Message[],
  apiKey: string
) {
  // === 核心修复 2：只要开启流式对话，第一件事就是让上一段语音直接闭嘴 ===
  interruptSpeakCharacter();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey || "ollama"}`,
  };

  const res = await fetch("http://localhost:11434/v1/chat/completions", {
    headers: headers,
    method: "POST",
    body: JSON.stringify({
      model: OLLAMA_MODEL,
      messages: messages,
      stream: true, 
    }),
  });

  const reader = res.body?.getReader();
  if (res.status !== 200 || !reader) {
    throw new Error(`Ollama API Error: ${res.status}`);
  }

  const stream = new ReadableStream({
    async start(controller: ReadableStreamDefaultController) {
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            const trimmedLine = line.trim();
            if (!trimmedLine || trimmedLine === "data: [DONE]") continue;

            if (trimmedLine.startsWith("data: ")) {
              const jsonStr = trimmedLine.replace(/^data: /, "").trim();
              if (!jsonStr) continue;

              try {
                const json = JSON.parse(jsonStr);
                const messagePiece = json.choices[0]?.delta?.content;
                if (messagePiece !== undefined && messagePiece !== null) {
                  controller.enqueue(messagePiece);
                }
              } catch (error) {
                console.warn("解析碎片失败:", jsonStr);
              }
            }
          }
        }
      } catch (error) {
        controller.error(error);
      } finally {
        reader.releaseLock();
        controller.close();
      }
    },
  });

  return stream;
}
