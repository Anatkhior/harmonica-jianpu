import { Upload } from "lucide-react";

type FileUploaderProps = {
  disabled: boolean;
  onFileSelected: (file: File) => void;
};

export function FileUploader({ disabled, onFileSelected }: FileUploaderProps) {
  return (
    <label className="upload-button" aria-disabled={disabled}>
      <Upload size={18} aria-hidden="true" />
      上传乐谱
      <input
        type="file"
        accept=".musicxml,.xml,.mxl"
        disabled={disabled}
        onChange={(event) => {
          const file = event.target.files?.[0];
          if (file) {
            onFileSelected(file);
          }
          event.target.value = "";
        }}
      />
    </label>
  );
}
