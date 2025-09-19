import { toast } from "react-toastify";

export const SuccessToast = (message : string) => toast.success(message);
export const ErrorToast = (message : string) => toast.error(message);
export const WarningToast = (message : string) => toast.info(message);
export const PromiseToast = <T>(promise: Promise<T>, messages: {
    pending: string;
    success: string;
    error: string;
}) => {
    return toast.promise(promise, {
        pending: messages.pending,
        success: messages.success,
        error: messages.error
    });
};