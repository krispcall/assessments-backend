import { toast } from "sonner";
export const showToast = (
  type: "success" | "error" | "info" | "warning",
  message: string
) => {
  switch (type) {
    case "success":
      return toast.success(message);
    case "error":
      return toast.error(message);
    case "info":
      return toast.info(message);
    case "warning":
      return toast.warning(message);
    default:
      return toast(message); // Default case if type is missing
  }
};
