import { useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { api, apiErrorMessage } from "../api/client";
import { AppShell } from "../components/AppShell";
import { Button, FieldError, FormError } from "../components/ui";

const schema = z.object({
  question: z.string().min(1, "Ask a question first"),
});

type FormValues = z.infer<typeof schema>;

type AgentResponse = {
  input?: string;
  output?: string;
  intermediate_steps?: unknown[];
  success?: boolean;
  error?: string;
};

type Turn = {
  id: number;
  question: string;
  response: AgentResponse | null;
  pending: boolean;
  errorMessage: string | null;
};

let turnId = 0;

export function ChatPage() {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [serverError, setServerError] = useState<string | null>(null);
  const listEndRef = useRef<HTMLDivElement | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const scrollToBottom = () => {
    requestAnimationFrame(() => {
      listEndRef.current?.scrollIntoView({ behavior: "smooth" });
    });
  };

  const onSubmit = async ({ question }: FormValues) => {
    setServerError(null);
    turnId += 1;
    const id = turnId;

    setTurns((prev) => [
      ...prev,
      { id, question, response: null, pending: true, errorMessage: null },
    ]);
    reset({ question: "" });
    scrollToBottom();

    try {
      const { data } = await api.post<AgentResponse>("/ai/query", { question });
      setTurns((prev) =>
        prev.map((t) =>
          t.id === id ? { ...t, response: data, pending: false } : t,
        ),
      );
    } catch (err) {
      const message = apiErrorMessage(err, "Query failed");
      setTurns((prev) =>
        prev.map((t) =>
          t.id === id ? { ...t, pending: false, errorMessage: message } : t,
        ),
      );
      setServerError(message);
    } finally {
      scrollToBottom();
    }
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-50">
            Ask your database
          </h2>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Ask a question in plain English. The agent will generate SQL, run it, and summarize the result.
          </p>
        </div>

        <FormError>{serverError}</FormError>

        <div className="space-y-4">
          {turns.length === 0 && (
            <div className="rounded-lg border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400">
              Try: <em>Show the top 5 customers by revenue</em> or <em>How many rows are in each table?</em>
            </div>
          )}

          {turns.map((turn) => (
            <TurnBubble key={turn.id} turn={turn} />
          ))}
          <div ref={listEndRef} />
        </div>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="sticky bottom-0 -mx-6 border-t border-slate-200 bg-slate-50/95 px-6 py-4 backdrop-blur dark:border-slate-800 dark:bg-slate-950/95"
          noValidate
        >
          <div className="flex items-start gap-3">
            <div className="flex-1">
              <textarea
                {...register("question")}
                rows={2}
                placeholder="Ask a question about your data..."
                className="block w-full resize-y rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm placeholder:text-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:placeholder:text-slate-500"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(onSubmit)();
                  }
                }}
              />
              <FieldError>{errors.question?.message}</FieldError>
            </div>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Sending…" : "Send"}
            </Button>
          </div>
        </form>
      </div>
    </AppShell>
  );
}

function TurnBubble({ turn }: { turn: Turn }) {
  return (
    <div className="space-y-2">
      <div className="flex justify-end">
        <div className="max-w-2xl rounded-lg bg-indigo-600 px-4 py-2 text-sm text-white shadow-sm">
          {turn.question}
        </div>
      </div>

      <div className="flex justify-start">
        <div className="w-full max-w-3xl rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm text-slate-800 shadow-sm dark:border-slate-800 dark:bg-slate-900 dark:text-slate-100">
          {turn.pending && <span className="text-slate-500">Thinking…</span>}

          {!turn.pending && turn.errorMessage && (
            <div className="text-red-600 dark:text-red-400">{turn.errorMessage}</div>
          )}

          {!turn.pending && turn.response && <AgentResponseView data={turn.response} />}
        </div>
      </div>
    </div>
  );
}

function AgentResponseView({ data }: { data: AgentResponse }) {
  if (data.success === false && data.error) {
    return <div className="text-red-600 dark:text-red-400">{data.error}</div>;
  }
  if (data.output) {
    return <pre className="whitespace-pre-wrap break-words font-sans">{data.output}</pre>;
  }
  return (
    <pre className="max-h-96 overflow-auto rounded bg-slate-100 p-3 text-xs text-slate-800 dark:bg-slate-950 dark:text-slate-200">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
