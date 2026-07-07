import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate } from "react-router-dom";
import { api, apiErrorMessage } from "../api/client";
import { AppShell } from "../components/AppShell";
import { Button, Card, FieldError, FormError, Input, Label } from "../components/ui";

type ConnectionResponse = {
  id: number;
  connection_name: string;
  db_type: string;
  host: string;
  port: number;
  database_name: string;
  username: string;
  is_active: boolean;
  is_verified: boolean;
};

const schema = z.object({
  connection_name: z.string().min(1, "Name is required").max(100),
  host: z.string().min(1, "Host is required"),
  port: z.number({ error: "Port is required" }).int().positive().max(65535),
  database_name: z.string().min(1, "Database name is required"),
  username: z.string().min(1, "Username is required"),
  password: z.string().min(1, "Password is required"),
  db_type: z.string().min(1),
});

type FormValues = z.infer<typeof schema>;

export function DatabaseConnectPage() {
  const navigate = useNavigate();
  const [existing, setExisting] = useState<ConnectionResponse | null>(null);
  const [loadingExisting, setLoadingExisting] = useState(true);
  const [serverError, setServerError] = useState<string | null>(null);
  const [testMessage, setTestMessage] = useState<string | null>(null);
  const [testing, setTesting] = useState(false);

  const {
    register,
    handleSubmit,
    getValues,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      connection_name: "",
      host: "",
      port: 3306,
      database_name: "",
      username: "",
      password: "",
      db_type: "mysql",
    },
  });

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const { data } = await api.get<ConnectionResponse>("/database");
        if (cancelled) return;
        setExisting(data);
        reset({
          connection_name: data.connection_name,
          host: data.host,
          port: data.port,
          database_name: data.database_name,
          username: data.username,
          password: "",
          db_type: data.db_type,
        });
      } catch {
        // No connection yet — expected on first visit.
      } finally {
        if (!cancelled) setLoadingExisting(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [reset]);

  const runTest = async () => {
    setTestMessage(null);
    setServerError(null);
    const values = getValues();
    setTesting(true);
    try {
      const { data } = await api.post<{ message: string }>("/database/test", {
        host: values.host,
        port: values.port,
        database_name: values.database_name,
        username: values.username,
        password: values.password,
      });
      setTestMessage(data.message);
    } catch (err) {
      setServerError(apiErrorMessage(err, "Connection test failed"));
    } finally {
      setTesting(false);
    }
  };

  const onSubmit = async (values: FormValues) => {
    setServerError(null);
    setTestMessage(null);
    try {
      await api.post<ConnectionResponse>("/database/connect", values);
      navigate("/chat", { replace: true });
    } catch (err) {
      setServerError(apiErrorMessage(err, "Failed to save connection"));
    }
  };

  return (
    <AppShell>
      <div className="mx-auto max-w-3xl">
        <div className="mb-4">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-50">
            {existing ? "Update database connection" : "Connect your database"}
          </h2>
        </div>
        <Card className="max-w-none">
          {loadingExisting ? (
            <p className="text-sm text-slate-500">Loading…</p>
          ) : (
            <form className="space-y-5" onSubmit={handleSubmit(onSubmit)} noValidate>
              {existing && (
                <div className="rounded-md border border-emerald-300 bg-emerald-50 px-3 py-2 text-sm text-emerald-800 dark:border-emerald-800/60 dark:bg-emerald-950/40 dark:text-emerald-200">
                  Editing existing connection: <strong>{existing.connection_name}</strong>. Re-enter the password to save changes.
                </div>
              )}

              <FormError>{serverError}</FormError>
              {testMessage && (
                <div className="rounded-md border border-emerald-300 bg-emerald-50 px-3 py-2 text-sm text-emerald-800 dark:border-emerald-800/60 dark:bg-emerald-950/40 dark:text-emerald-200">
                  {testMessage}
                </div>
              )}

              <div>
                <Label htmlFor="connection_name">Connection name</Label>
                <Input id="connection_name" {...register("connection_name")} />
                <FieldError>{errors.connection_name?.message}</FieldError>
              </div>

              <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
                <div className="sm:col-span-3">
                  <Label htmlFor="host">Host</Label>
                  <Input id="host" placeholder="db.example.com" {...register("host")} />
                  <FieldError>{errors.host?.message}</FieldError>
                </div>
                <div>
                  <Label htmlFor="port">Port</Label>
                  <Input id="port" type="number" {...register("port", { valueAsNumber: true })} />
                  <FieldError>{errors.port?.message}</FieldError>
                </div>
              </div>

              <div>
                <Label htmlFor="database_name">Database name</Label>
                <Input id="database_name" {...register("database_name")} />
                <FieldError>{errors.database_name?.message}</FieldError>
              </div>

              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <Label htmlFor="username">Username</Label>
                  <Input id="username" autoComplete="off" {...register("username")} />
                  <FieldError>{errors.username?.message}</FieldError>
                </div>
                <div>
                  <Label htmlFor="password">Password</Label>
                  <Input id="password" type="password" autoComplete="new-password" {...register("password")} />
                  <FieldError>{errors.password?.message}</FieldError>
                </div>
              </div>

              <div>
                <Label htmlFor="db_type">Database type</Label>
                <Input id="db_type" {...register("db_type")} />
                <FieldError>{errors.db_type?.message}</FieldError>
              </div>

              <div className="flex flex-wrap items-center gap-3 pt-2">
                <Button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? "Saving…" : existing ? "Update connection" : "Save connection"}
                </Button>
                <Button
                  type="button"
                  onClick={runTest}
                  disabled={testing}
                  className="!bg-slate-200 !text-slate-900 hover:!bg-slate-300 dark:!bg-slate-800 dark:!text-slate-100 dark:hover:!bg-slate-700"
                >
                  {testing ? "Testing…" : "Test connection"}
                </Button>
              </div>
            </form>
          )}
        </Card>
      </div>
    </AppShell>
  );
}
