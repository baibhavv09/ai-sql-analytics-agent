import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate } from "react-router-dom";
import { AuthLayout } from "../components/AuthLayout";
import { Button, Card, FieldError, FormError, Input, Label } from "../components/ui";
import { useAuth } from "../auth/AuthContext";
import { apiErrorMessage } from "../api/client";

const schema = z.object({
  full_name: z.string().min(1, "Full name is required"),
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "At least 8 characters"),
});

type FormValues = z.infer<typeof schema>;

export function RegisterPage() {
  const { register: registerUser, login } = useAuth();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const onSubmit = async (values: FormValues) => {
    setServerError(null);
    try {
      await registerUser(values.full_name, values.email, values.password);
      await login(values.email, values.password);
      navigate("/", { replace: true });
    } catch (err) {
      setServerError(apiErrorMessage(err, "Registration failed"));
    }
  };

  return (
    <AuthLayout title="Create an account" subtitle="Start querying your database with natural language">
      <Card>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)} noValidate>
          <FormError>{serverError}</FormError>

          <div>
            <Label htmlFor="full_name">Full name</Label>
            <Input id="full_name" autoComplete="name" {...register("full_name")} />
            <FieldError>{errors.full_name?.message}</FieldError>
          </div>

          <div>
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" autoComplete="email" {...register("email")} />
            <FieldError>{errors.email?.message}</FieldError>
          </div>

          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              autoComplete="new-password"
              {...register("password")}
            />
            <FieldError>{errors.password?.message}</FieldError>
          </div>

          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? "Creating account…" : "Create account"}
          </Button>
        </form>
      </Card>

      <p className="mt-4 text-center text-sm text-slate-600 dark:text-slate-400">
        Already have an account?{" "}
        <Link to="/login" className="font-medium text-indigo-600 hover:underline dark:text-indigo-400">
          Sign in
        </Link>
      </p>
    </AuthLayout>
  );
}
