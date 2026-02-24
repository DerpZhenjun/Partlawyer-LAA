import { useEffect, useRef } from "react";
import { Message } from "@/features/messages/messages";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";

type Props = {
  messages: Message[];
};

export const ChatLog = ({ messages }: Props) => {
  const chatScrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatScrollRef.current?.scrollIntoView({ behavior: "auto", block: "center" });
  }, []);

  useEffect(() => {
    chatScrollRef.current?.scrollIntoView({ behavior: "smooth", block: "center" });
  }, [messages]);

  return (
    <div className="absolute w-col-span-6 max-w-full h-[100svh] pb-64">
      <div className="max-h-full px-16 pt-104 pb-64 overflow-y-auto scroll-hidden">
        {messages.map((msg, i) => {
          return (
            <div key={i} ref={messages.length - 1 === i ? chatScrollRef : null}>
              <Chat role={msg.role} message={msg.content || ""} />
            </div>
          );
        })}
      </div>
    </div>
  );
};

const Chat = ({ role, message }: { role: string; message: string }) => {
  const roleColor = role === "assistant" ? "bg-secondary text-white" : "bg-base text-primary";
  const roleText = role === "assistant" ? "text-gray-900" : "text-primary";
  const offsetX = role === "user" ? "pl-40" : "pr-40";

  let displayMessage = message || "";
  if (role === "assistant") {
    // 1. 处理思考标签（转化为引用框）
    if (displayMessage.includes("<think>")) {
      displayMessage = displayMessage.replace(/<think>/gi, "> *🧠 阿律的内心戏：*\n> *");
      displayMessage = displayMessage.replace(/<\/think>/gi, "*\n\n---\n\n");
    }

    // === 2. 终极排版纠错装甲：强行打断所有不规范的粘连 ===
    
    // 拦截 A：如果句号后面跟着“加粗文字”（通常是标题），强制换行
    displayMessage = displayMessage.replace(/([。！？；>])\s*(?=\*\*)/g, "$1\n\n");
    
    // 拦截 B：如果句号后面跟着“中文+冒号”（例如“冲突点：”），强制换行
    displayMessage = displayMessage.replace(/([。！？；>])\s*(?=[\u4e00-\u9fa5]+[：:])/g, "$1\n\n");
    
    // 拦截 C：如果句号后面跟着“数字.”或者“-”（列表），强制换行
    displayMessage = displayMessage.replace(/([。！？；>])\s*(?=\d+\.|-)/g, "$1\n\n");
    
    // 拦截 D：修复大模型忘记在列表符后加空格的毛病 (比如把 "1.身份" 变成 "1. 身份")
    displayMessage = displayMessage.replace(/(\n\d+)\.([^\s])/g, "$1. $2");
    displayMessage = displayMessage.replace(/(\n-)([^\s])/g, "$1 $2");
  }

  return (
    <div className={`mx-auto max-w-sm my-16 ${offsetX}`}>
      <div className={`px-24 py-8 rounded-t-8 font-bold tracking-wider ${roleColor}`}>
        {role === "assistant" ? "CHARACTER" : "YOU"}
      </div>
      <div className="px-24 py-16 bg-white rounded-b-8 shadow-sm">
        <div className={`
          text-[15px] leading-relaxed break-words ${roleText}
          [&>*:first-child]:mt-0 [&>*:last-child]:mb-0
          
          [&_p]:mb-3 
          
          [&_h1]:text-xl [&_h1]:font-bold [&_h1]:mt-5 [&_h1]:mb-3 [&_h1]:text-black
          [&_h2]:text-lg [&_h2]:font-bold [&_h2]:mt-4 [&_h2]:mb-2 [&_h2]:text-black
          [&_h3]:text-base [&_h3]:font-bold [&_h3]:mt-3 [&_h3]:mb-1 [&_h3]:text-black
          
          [&_ul]:list-disc [&_ul]:list-outside [&_ul]:ml-5 [&_ul]:mb-3 [&_ul]:space-y-1
          [&_ol]:list-decimal [&_ol]:list-outside [&_ol]:ml-5 [&_ol]:mb-3 [&_ol]:space-y-1
          [&_li]:list-item
          
          [&_strong]:font-bold [&_strong]:text-black
          
          [&_blockquote]:border-l-4 [&_blockquote]:border-gray-300 [&_blockquote]:pl-3 [&_blockquote]:py-1 [&_blockquote]:my-3 [&_blockquote]:text-gray-500 [&_blockquote]:bg-gray-50 [&_blockquote]:italic
          
          [&_hr]:my-4 [&_hr]:border-gray-200 [&_hr]:border-dashed
        `}>
          {displayMessage.trim() ? (
            <ReactMarkdown 
              remarkPlugins={[remarkGfm, remarkBreaks]}
            >
              {displayMessage}
            </ReactMarkdown>
          ) : role === "assistant" ? (
            <span className="animate-pulse text-gray-400 font-normal">阿律正在思考中...</span>
          ) : (
            <span className="animate-pulse text-gray-400">...</span>
          )}
        </div>
      </div>
    </div>
  );
};