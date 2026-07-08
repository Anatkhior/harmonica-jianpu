import { useRef } from "react";
import { Upload } from "lucide-react";

type FileUploaderProps = {
  disabled: boolean;
  onFileSelected: (file: File) => void;
};

export function FileUploader({ disabled, onFileSelected }: FileUploaderProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  return (
    <>
      <button
        className="upload-button"
        disabled={disabled}
        type="button"
        onClick={() => inputRef.current?.click()}
      >
        <Upload size={18} aria-hidden="true" />
        上传乐谱
      </button>
      <input
        ref={inputRef}
        className="visually-hidden-file"
        type="file"
        accept=".musicxml,.xml,.mxl,.pdf,.jpg,.jpeg,.png"
        disabled={disabled}
        onChange={(event) => {
          const file = event.target.files?.[0];
          if (file) {
            onFileSelected(file);
          }
          event.target.value = "";
        }}
      />
    </>
  );
}
