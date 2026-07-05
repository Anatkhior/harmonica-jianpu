type ErrorNoticeProps = {
  message: string;
};

export function ErrorNotice({ message }: ErrorNoticeProps) {
  if (!message) {
    return null;
  }

  return (
    <p className="notice" role="alert">
      {message}
    </p>
  );
}
